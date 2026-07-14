---
title: "Event 2"
date: 2026-06-06
weight: 3
chapter: false
pre: " <b> 4.3. </b> "
---

# Bài thu hoạch "FCAJ Community Day 2026"

### Thông Tin Sự Kiện

- **Tên sự kiện:** FCAJ Community Day 2026
- **Thời gian:** Thứ Bảy, ngày 06/06/2026
- **Địa điểm:** Bitexco Financial Tower, Thành phố Hồ Chí Minh
- **Vai trò trong sự kiện:** Người tham dự

### Mục Đích Của Sự Kiện

FCAJ Community Day tháng 6 được tổ chức nhằm chia sẻ những kiến thức và kinh nghiệm thực tế trong các lĩnh vực Cloud Computing, AI, DevOps, Cyber Security và phát triển phần mềm trên nền tảng AWS. Thông qua các phiên trình bày từ những kỹ sư và diễn giả đang làm việc trong ngành, người tham dự có cơ hội tiếp cận các công nghệ mới, hiểu rõ hơn về cách xây dựng hệ thống trên AWS và định hướng nghề nghiệp trong lĩnh vực công nghệ thông tin.

Ngoài việc cập nhật kiến thức chuyên môn, sự kiện còn tạo điều kiện để sinh viên giao lưu với cộng đồng AWS, học hỏi kinh nghiệm từ các dự án thực tế và mở rộng góc nhìn về những kỹ năng cần thiết khi làm việc trong môi trường doanh nghiệp.

### Nội Dung Chính

#### Docker - A Containerization Technology

**Diễn giả:** Anh Bảo Huỳnh

Chủ đề đầu tiên tập trung vào vấn đề triển khai ứng dụng sao cho ổn định trên nhiều môi trường khác nhau. Virtual Machine truyền thống thường tiêu tốn nhiều tài nguyên vì mỗi máy ảo cần một hệ điều hành riêng, từ đó khiến việc triển khai và mở rộng nhiều ứng dụng trở nên nặng hơn.

Docker được giới thiệu như một công nghệ containerization giúp đóng gói ứng dụng cùng môi trường chạy vào một container. Nhờ vậy, ứng dụng có thể hoạt động nhất quán trên nhiều môi trường với tinh thần "Build once, Run anywhere". Diễn giả cũng giải thích Docker Image, Docker Container, Dockerfile, các lệnh Docker cơ bản và những ứng dụng phổ biến trong CI/CD, microservices và cloud native development.

Giá trị thực tế của Docker là giúp nhóm phát triển triển khai phần mềm hiệu quả hơn, giảm lỗi do khác biệt môi trường và hỗ trợ tốt hơn cho các workflow phát triển cloud hiện đại.

#### Combining AWS WAF with Machine Learning for Cyber Attack Detection

**Diễn giả:** Anh Lê Hoàng Gia Đại

Chủ đề này nói về hạn chế của các Web Application Firewall truyền thống. Cách phát hiện dựa trên rule có thể bảo vệ hệ thống trước các mẫu tấn công đã biết, nhưng sẽ gặp khó khăn hơn khi đối mặt với các kiểu tấn công mới hoặc hành vi bất thường chưa có trong bộ luật.

Giải pháp được trình bày là xây dựng hệ thống Network Intrusion Detection System (NIDS) sử dụng Machine Learning để phân tích lưu lượng mạng và phát hiện hành vi bất thường. Mô hình được huấn luyện bằng bộ dữ liệu CSE-CIC-IDS2018 và triển khai trên AWS với các dịch vụ như Amazon EC2, AWS WAF, Lambda, CloudWatch, Security Hub và Amazon SNS.

Qua phần này, tôi hiểu rõ hơn cách Machine Learning có thể bổ sung cho AWS WAF để tăng khả năng phát hiện và cảnh báo tấn công theo thời gian thực. Với doanh nghiệp, hướng tiếp cận này giúp tăng cường bảo mật ứng dụng và giảm rủi ro bỏ sót các hoạt động mạng đáng nghi.

#### Multiplayer in the Cloud: Connecting Godot Clients with AWS WebSockets

**Diễn giả:** Anh Nguyễn Quốc Bảo

Chủ đề thứ ba nói về bài toán xây dựng giao tiếp thời gian thực cho game multiplayer. Các cách giao tiếp như HTTP polling có thể không phù hợp với ứng dụng cần cập nhật hai chiều nhanh giữa nhiều người dùng.

Diễn giả giới thiệu kiến trúc multiplayer game sử dụng AWS WebSocket. Hệ thống dùng API Gateway WebSocket kết hợp với AWS Lambda và Amazon DynamoDB để quản lý kết nối giữa người chơi. Lambda xử lý logic kết nối, ghép cặp và đồng bộ dữ liệu, trong khi DynamoDB lưu trạng thái của từng phiên kết nối.

Giá trị thực tế của kiến trúc này là cho thấy các dịch vụ serverless của AWS có thể hỗ trợ ứng dụng thời gian thực. Nội dung này cũng giúp tôi hiểu WebSocket không chỉ dùng cho game, mà còn có thể áp dụng cho chat, công cụ cộng tác trực tuyến và các ứng dụng tương tác khác.

#### The Art of Effective Teamwork

**Diễn giả:** Anh Trương Huy Phước

Bên cạnh các chủ đề kỹ thuật, phần chia sẻ này tập trung vào một vấn đề rất thường gặp trong dự án: công nghệ tốt chưa đủ nếu nhóm thiếu mục tiêu chung, giao tiếp rõ ràng và trách nhiệm cá nhân.

Diễn giả chia sẻ bốn nguyên tắc quan trọng trong làm việc nhóm, gồm xác định mục tiêu chung rõ ràng, phân chia công việc phù hợp với từng thành viên, duy trì giao tiếp hiệu quả và đề cao trách nhiệm cá nhân. Một số công cụ hỗ trợ quản lý công việc cũng được nhắc đến như Trello, ClickUp, Google Workspace, Slack và Discord.

Giá trị của chủ đề này rất thực tế với các dự án sinh viên. Nó nhắc tôi rằng một sản phẩm phần mềm thành công không chỉ phụ thuộc vào khả năng lập trình, mà còn phụ thuộc vào sự phối hợp, tinh thần sở hữu công việc và giao tiếp giữa các thành viên.

#### Build GraphRAG Applications using Amazon Bedrock and Amazon Neptune

**Diễn giả:** Anh Việt Phát

Chủ đề này giới thiệu GraphRAG như một cách cải thiện Retrieval-Augmented Generation khi câu hỏi cần nhiều bước suy luận. RAG truyền thống có thể bị giới hạn nếu chỉ truy xuất các đoạn văn bản mà chưa hiểu mối quan hệ giữa các thực thể.

Diễn giả giải thích cách GraphRAG kết hợp Amazon Bedrock với Amazon Neptune. Amazon Neptune có thể lưu trữ quan hệ giữa các thực thể dưới dạng graph data, còn Amazon Bedrock cung cấp foundation model để hỗ trợ suy luận và tạo câu trả lời. Cách tiếp cận này giúp hệ thống AI sử dụng thông tin có liên kết thay vì chỉ dựa trên tìm kiếm văn bản thông thường.

Giá trị thực tế là cải thiện chất lượng câu trả lời cho các ứng dụng AI cần suy luận dựa trên quan hệ dữ liệu. Điều này phù hợp với các hệ thống tri thức, enterprise search và những ứng dụng cần hiểu kết nối giữa nhiều điểm dữ liệu.

#### From IT Helpdesk to Senior Sysadmin

**Diễn giả:** Anh Trần Trung Vinh

Phần chia sẻ cuối tập trung vào phát triển nghề nghiệp, đặc biệt là hành trình từ IT Helpdesk lên Senior System Administrator. Vấn đề được nhấn mạnh là nhiều người học muốn đi nhanh vào Cloud hoặc DevOps nhưng chưa có nền tảng đủ vững về Linux, networking và system administration.

Diễn giả nhấn mạnh tầm quan trọng của việc xây dựng nền tảng kỹ thuật trước khi tiếp cận cloud và DevOps. Anh cũng chia sẻ kinh nghiệm phỏng vấn, xây dựng dự án cá nhân và rèn luyện kỹ năng thực hành. Thông điệp làm tôi chú ý là chứng chỉ có giá trị, nhưng kinh nghiệm thực tế và dự án cá nhân mới là yếu tố giúp ứng viên tạo lợi thế rõ hơn khi ứng tuyển.

Giá trị của chủ đề này nằm ở định hướng nghề nghiệp. Nó giúp tôi thấy rằng để phát triển lâu dài trong cloud và DevOps, người học cần liên tục học tập, thực hành và củng cố nền tảng kỹ thuật.

### Những Gì Học Được

- Tôi hiểu rõ hơn sự khác biệt giữa Virtual Machine và Docker Container, cũng như vai trò của Docker trong triển khai ứng dụng cloud native.
- Tôi biết cách AWS WAF có thể kết hợp với Machine Learning để tăng khả năng phát hiện tấn công mạng và nâng cao bảo mật hệ thống.
- Tôi hiểu kiến trúc xây dựng ứng dụng thời gian thực bằng API Gateway WebSocket, AWS Lambda và Amazon DynamoDB.
- Tôi nhận ra tầm quan trọng của giao tiếp, phân chia công việc và trách nhiệm cá nhân trong quá trình làm việc nhóm.
- Tôi có thêm kiến thức về GraphRAG, Amazon Bedrock và Amazon Neptune trong việc phát triển các ứng dụng AI hiện đại.
- Tôi hiểu rằng học tập liên tục, thực hành trên dự án thực tế và xây dựng nền tảng vững chắc là yếu tố quan trọng để phát triển sự nghiệp trong Cloud Computing và DevOps.

### Ứng Dụng Vào Công Việc

Kiến thức từ sự kiện này hữu ích cho dự án **AWS Serverless Event Portal** của tôi vì nhiều chủ đề liên quan trực tiếp đến backend services, kiến trúc AWS và cách phối hợp trong project. Phần WebSocket giúp tôi hiểu rõ hơn cách API Gateway, Lambda và DynamoDB có thể hỗ trợ giao tiếp thời gian thực, dù project hiện tại của tôi chưa triển khai multiplayer hoặc live messaging.

Chủ đề Docker cũng giúp tôi hiểu vì sao môi trường chạy nhất quán lại quan trọng khi phát triển và triển khai ứng dụng. Trong các cải tiến sau này, kiến thức này có thể hỗ trợ quy trình phát triển backend gọn hơn và giúp chuẩn bị service dễ triển khai hơn.

Phần bảo mật nhắc tôi rằng ứng dụng web sau khi triển khai cần được bảo vệ và giám sát. Dù tôi chưa xây dựng hệ thống Machine Learning để phát hiện tấn công trong project, nội dung này giúp tôi quan tâm hơn đến AWS WAF, monitoring, cảnh báo và kiến trúc an toàn.

GraphRAG cũng cho tôi thêm ý tưởng về hướng tích hợp AI trong tương lai. Nếu Event Portal sau này cần tính năng như tìm kiếm tri thức sự kiện hoặc hỗ trợ thông minh hơn, Amazon Bedrock và dữ liệu dạng graph có thể là hướng đáng tìm hiểu, nhưng không có nghĩa là các tính năng này đã được triển khai trong project hiện tại.

### Trải nghiệm trong event

Điều làm tôi ấn tượng nhất trong sự kiện là sự đa dạng của các chủ đề. Các phần chia sẻ đi từ containerization, bảo mật, ứng dụng thời gian thực đến làm việc nhóm, kiến trúc AI và phát triển nghề nghiệp. Điều này làm cho event khá cân bằng vì vừa có kỹ năng kỹ thuật vừa có góc nhìn phát triển bản thân.

Tôi đặc biệt thấy phần WebSocket và GraphRAG hữu ích vì chúng gắn các dịch vụ AWS với những tình huống ứng dụng cụ thể. Các ví dụ này giúp tôi thấy cách API Gateway, Lambda, DynamoDB, Bedrock và Neptune có thể phối hợp tùy theo bài toán cần giải quyết.

Phần chia sẻ nghề nghiệp cũng tạo thêm động lực để tôi tiếp tục củng cố nền tảng. Sau sự kiện, tôi cảm thấy việc học AWS nên đi cùng với thực hành Linux, networking, system administration, kỹ năng làm việc nhóm và xây dựng dự án thực tế.

#### Một số hình ảnh khi tham gia sự kiện

![Ảnh tham gia FCAJ Community Day 2026](/images/4-EventParticipated/4.3-Event3/fcaj-community-day-2026-event3.jpg)

> Tổng thể, sự kiện giúp tôi kết nối các kiến thức về AWS cloud services, AI, bảo mật, làm việc nhóm và định hướng nghề nghiệp theo hướng thực tế hơn.