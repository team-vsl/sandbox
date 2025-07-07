# VP Bank Hackathon - Challenge 23 Solution

Mã nguồn giải pháp cho Challenge 23.

## Collaborators

Update later...

## Requirements

Khi phát triển thì yêu cầu một số điều kiện sau:

1. Phát triển trên môi trường Linux.
2. Cài AWS CLI.
3. Cài Python (>3.1x).

## How to setup ?

Hướng dẫn thiết lập một số thứ

### AWS CLI

1. Đăng nhập vào trong IAM User đã được đưa và tạo Access Key và Secret Key.
2. Sau đó là setup profile trong AWS CLI (Nhớ cài AWS CLI).

```bash
aws configure --profile vsl
```

Sau đó là lần lượt thêm Access Key ID, Access Secret Key, Region = `ap-southeast-1`, Output = `json`.

### Setup environment file

1. Vào trong thư mục dự án, tạo file `.env`
2. Copy toàn bộ nội dung của `.env.example` sang `.env`.
3. Điền những thông tin còn thiếu là xong.

Hoặc là dùng lệnh này để làm nhanh các bước trên:

```bash
cat .env.example > .env
```

### Create DataContract Temporary Directory

1. Ở home của user, tạo một thư mục theo đường dẫn sau.

```bash
sudo mkdir -p /var/vpbank/datacontracts
```

2. Sau đó thì thêm toàn quyền cho folder này.

```bash
sudo chmod -R 777 /var/vpbank/datacontracts
```

### Project

1. Đầu tiên là phải tải >= python3, pip3.
2. Tải thêm thư viện python3-venv.
3. Tạo môi trường ảo cho dự án.

```bash
python3 -m venv venv
```

4. Cài packages

```bash
pip install -r requirements.txt
```

5. Xong
