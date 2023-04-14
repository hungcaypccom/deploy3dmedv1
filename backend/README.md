###
Cài đặt môi trường: 
###
python 3.9
cài poetry
cài dependency từ file requirements.txt
run server: "poetry run start"

###
Config
###

- config main: 
+ config database: DB_CONFIG = f"postgresql+asyncpg://postgres:1234567890@localhost:5432/test"
+ config JWT

- alembic.ini:
+ config database: sqlalchemy.url = postgresql+asyncpg://postgres:1234567890@localhost:5432/test
+ alembic revision --autogenerate -m "init migration": convert từ object sang table lần đầu tiên để tạo table trong database (chỉ chạy lần đầu tiên)
Sau khi tạo chạy lệnh này sẽ sinh ra 1 file .py trong "migrations/ versions"
Vào file py import thư viện: "import sqlmodel"
# alembic revision --autogenerate -m "Add inital tables": không xài
+ alembic upgrade heads: chạy lệnh này sau lên init để đồng bộ xuống database (chỉ chạy 1 lần)

- config auto_download module ( tự động download từ server hans)
- config client_download module (download service tới end-user)
- config hans3d module

###
API
###

User_API:
- users : không tham số, trả về thông tin người dùng, lưu ý, nếu date_end lớn hơn 1 năm thì hiển thị là vĩnh viễn
- edit-profile: thay đổi thông tin người dùng, hiển thị thông tin cũ từ cũ từ users cho khách khỏi nhập lại những thông tin k muốn đổi, bắt buộc nhập đúng mk cũ
- download-file: tải file theo tên truyền vào
- data-info-total-count: đếm tổng số infodata để tiện việc phân trang ( biến downloadable = True là filter những infodata có thể download được, downloadable = Flase là filter tất cả)
- data-info-pagging: trả về infodata ( biến downloadable = True là filter những infodata có thể download được, downloadable = Flase là filter tất cả). Lưu ý check biến "downloadable"
nếu False thì k bấm được nút download
- delete-file: truyền vào 1 list json - xoá data lưu trên server theo tên trong list. Khi xoá biến downloadable sẽ set False và k thể phục hồi

Admin_API:
- register: tạo tài khoản mới ( tạo được cả admin và user)
- update-user-details: thay đổi thông tin người dùng
- forgot-password: cấp lại mật khẩu cho bất kỳ account nào
- find-info-by-status: tìm tất cả info-data bằng status True or False ( True là đã tải từ server hans về, False là chưa tải)
- find-info-by-downloadable: tìm tất cả info-data bằng downloadabe True or False (True là còn file trên server có thể tải)
- get - all -account: tìm tất cả account ( chỉ có ID và pass)
- data-info-find-all: tìm tất cả data-info
- user-details: truyền vào username, thông tin chi tiết của 1 user, kết hợp lưu thông tin cho api update-user-details
- user-all: toàn bộ thông tin chi tiết user
- data-info-total-count/ pagging: truyền vào username tìm thông tin như api của username 
- delete-file: truyền vào 1 list json - xoá data lưu trên server theo tên trong list. Khi xoá biến downloadable sẽ set False và k thể phục hồi
