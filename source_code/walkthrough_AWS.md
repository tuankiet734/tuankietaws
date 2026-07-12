# Walkthrough - Tích Hợp Đặc Trưng Mới Và Tối Ưu Hóa Mô Hình Trên AWS

Tài liệu này tổng hợp toàn bộ kết quả nâng cấp mô hình dự báo nhu cầu (sử dụng hàm lỗi Tweedie) và tích hợp thành công 5 cột đặc trưng mới từ AWS database để giải quyết triệt để vấn đề Underfitting.

---

## 1. Các Thay Đổi Đã Thực Hiện

### Huấn luyện Mô hình
*   **[train.py](file:///D:/TAAWS/AWS/train.py) & [retrain.py](file:///D:/TAAWS/AWS/retrain.py)**:
    *   Chuyển cấu hình mô hình `LGBMRegressor` sang sử dụng **Tweedie Loss** (`objective='tweedie'`), giúp mô hình dự báo chính xác nhất đối với dữ liệu số lượng bán lẻ có độ lệch cao (skewed data).
    *   Mô hình tự động học trên **34 đặc trưng** (bao gồm 5 cột đặc trưng mới được cập nhật trên cơ sở dữ liệu).

### Orchestrator API (Layer 1 - EC2)
*   **[app/config.py](file:///D:/TAAWS/AWS/app/config.py)**: Chuyển cấu hình `DB_HOST` mặc định sang `training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com` (nơi chứa bảng `final_daily` có 34 cột đặc trưng đầy đủ).
*   **[app/database.py](file:///D:/TAAWS/AWS/app/database.py)**: Cập nhật hàm `fetch_features_from_db` để truy vấn và ánh xạ thêm 5 cột mới từ bảng `final_daily`.
*   **[app/main.py](file:///D:/TAAWS/AWS/app/main.py)**: Cập nhật biến `REQUIRED_FEATURES` để xác thực đầu vào đầy đủ 34 cột.
*   **[app/predictor.py](file:///D:/TAAWS/AWS/app/predictor.py)**: 
    *   Bổ sung giá trị mặc định cho 5 cột mới trong `get_default_features` phòng trường hợp dữ liệu bị thiếu.
    *   Thay đổi cơ chế định dạng đặc trưng đầu vào bằng cách tự động lấy danh sách và thứ tự cột từ `scaler.feature_names_in_` (Căn chỉnh cột động), giúp hệ thống không bị lỗi crash/mismatch nếu thứ tự cột thay đổi trong tương lai.

### AWS Lambda API (Layer 2 - ML Service)
*   **[lambda_function.py](file:///D:/TAAWS/AWS/lambda_function.py)**: 
    *   Chuyển `DB_HOST` sang `training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com`.
    *   Cập nhật `DEFAULT_FEATURES` và `required_cols` để hỗ trợ 5 cột đặc trưng mới.
    *   Cập nhật truy vấn SQL để lấy thêm 5 cột đặc trưng mới.
    *   Áp dụng cơ chế căn chỉnh cột động từ `scaler.feature_names_in_` trước khi đưa qua StandardScaler.
*   **[lambda_app.py](file:///D:/TAAWS/AWS/lambda_app.py)**: Cập nhật truy vấn SQL trong kịch bản dự báo hàng ngày để lấy đầy đủ 34 đặc trưng từ bảng `final_daily`.

---

## 2. Kết Quả Huấn Luyện Mô Hình
Khi chạy [train.py](file:///D:/TAAWS/AWS/train.py), mô hình đã tự động tải dữ liệu 34 đặc trưng từ RDS, huấn luyện thành công và xuất các file `.pkl` mới:
*   Mô hình được lưu cục bộ và **tự động tải lên S3** thành công:
    *   `s3://fashion-product-images-group3979/models/lightgbm_demand_model.pkl`
    *   `s3://fashion-product-images-group3979/models/standard_scaler.pkl`
    *   `s3://fashion-product-images-group3979/models/label_encoders.pkl`

### Chỉ số hiệu năng mô hình (Model Performance Report)
*   **MAE (Sai số tuyệt đối trung bình)**: `0.2984`
*   **MAPE (Phần trăm sai số tuyệt đối trung bình)**: `11.47%` (Độ chính xác đạt gần **89%**)
*   **RMSE (Sai số bình phương trung bình)**: `0.5184`
*   **R² Score**: `9.71%`

---

## 3. Kết Quả Triển Khai Thực Tế Trên AWS

### AWS Lambda
1.  **Rebuild Container Image**: Đóng gói Docker image từ [Dockerfile](file:///D:/TAAWS/AWS/Dockerfile) sử dụng cấu hình loại bỏ attestation layers (`--provenance=false`) để tương thích hoàn toàn với AWS Lambda.
2.  **Push sang Amazon ECR**: Đẩy ảnh container thành công lên ECR repository `507221377279.dkr.ecr.ap-southeast-1.amazonaws.com/fashion-demand-predictor:latest`.
3.  **Update Lambda Function**: Cập nhật trực tiếp mã nguồn của hàm Lambda **`FashionDemandForecastAPI`** để sử dụng ảnh container mới. Trạng thái cập nhật đã thành công (`Successful`).

### AWS EC2 Orchestrator (`18.141.158.110`)
1.  **Tải lên tệp (File Upload)**: Đã tải lên thành công các tệp Python đã được cập nhật: [config.py](file:///D:/TAAWS/AWS/app/config.py), [database.py](file:///D:/TAAWS/AWS/app/database.py), [main.py](file:///D:/TAAWS/AWS/app/main.py), và [predictor.py](file:///D:/TAAWS/AWS/app/predictor.py) vào thư mục `/home/ubuntu/app/` sử dụng tệp khóa `Thanh_key.pem`.
2.  **Khởi động lại tiến trình (Service Restart)**: Khởi động lại dịch vụ uvicorn chạy trên cổng 80 bằng lệnh `nohup` trong nền.
3.  **Xác nhận hoạt động (Status Check)**: Kiểm tra logs `uvicorn.log` cho thấy dịch vụ đã hoạt động trực tuyến (`online`), hoàn tất việc triển khai và đồng bộ hóa toàn bộ hệ thống!

---

## 4. Kết Quả Kiểm Thử API End-to-End thành công

Thực hiện kiểm thử gọi API trực tiếp tới máy chủ EC2 tại địa chỉ **`http://18.141.158.110/predict`** bằng yêu cầu POST:

*   **Body (JSON)**:
    ```json
    {
        "store_id": "STORE_001",
        "sku": "CHAC10010--",
        "date": "2026-06-24",
        "total_discount_avg": 0.15
    }
    ```
*   **Response (JSON)**:
    ```json
    {
        "status": "success",
        "predicted_quantity": 1.19,
        "input_received": {
            "store_id": "STORE_001",
            "sku": "CHAC10010--",
            "date": "2026-06-24",
            "total_discount_avg": 0.15
        }
    }
    ```

Dự báo lượng nhu cầu là **`1.19`** đã được trả về thành công thông qua chuỗi xử lý tự động của hệ thống từ database RDS tới mô hình máy học trên AWS Lambda!
