# Test Module

Để có thể test, thì ae nên CD vào trong /test, vì các file script trong này đều setup sys.path có trở về level trước đó.

```py
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
```

Nghĩa là nếu như mình đang ở `/home/user/sandbox` thì nó sẽ về `/home/user` -> Không tìm thấy được mã nguồn. Nên là mình nên chạy nó ở trong `/home/user/sandbox/test` thì nó sẽ trả về là `/home/user/sandbox` -> Tìm thấy được mã nguồn.
