# Lambda Simulation

Để có thể test nhanh một số hàm lambda ở dưới local, thì mình có thể dùng tới phần này để có thể chạy Fast API.

## How to instal?

Thực hiện các bước sau để cài đặt các packages có trong `requirements.txt`.

0. Vào trong thư mục `simulation`

```bash
cd simulation
```

1. Tạo thư mục `packages`

```bash
mkdir packages
```

2. Thực hiện việc cài đặt, không dùng môi trường ảo nhé !!

```bash
pip3 install -r requirements.txt --target ./packages
```

## Start simulation

Để có thể chạy được giả lập lambda, thì làm theo các bước sau:

0. Vào trong thư mục `simulation`

```bash
cd simulation
```

> Note: nhớ tạo file `.env` theo file `.env.example`.

1. Chạy server fastapi

```bash
python main.py
```
