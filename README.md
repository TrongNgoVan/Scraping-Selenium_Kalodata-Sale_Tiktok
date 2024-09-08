![image](https://github.com/user-attachments/assets/18e0b9d4-bea3-4bb9-aca0-dae61df4008a)# Scraping_Selenium_Kalodata-Sale_Tiktok
Bước 1: 
  - Nhận dạng đặc điểm trang web
    + Đây là web API  cung cấp phương thức Get để lấy dữ liệu như cách thông thường.
    + Đây là web động bởi nếu bật tool vô hiệu hóa JavaScript thì ngay lập tức web sẽ không hiển thị dữ liệu ( hoặc có thể nhìn bằng mắt cách nó tải dữ liệu bằng Ajax mà nhận ra).     
    + Đây là web phải đăng nhập với những thao tác rườm rà hơn,đăng nhập nhiều lần cũng có khả năng bị chặn IP cao
    + Đây là web có số lượt tương tác để xem doanh thu giới hạn 10 lần/ngày, 7 ngày/ tài khoản , 30 ngày thống kê / mỗi lần xem.
    + Đây là web mà muốn xem được dữ liệu thì phải thực hiện những thao tác di chuột từ người dùng.
  - Xác định phương pháp Scraping:
    + Sử dụng thư viện Selenium sẽ giải quyết được những vấn đề như tự động hóa việc đăng nhập.
    + Tự động hóa trong việc click qua các chức năng để vào được trang cần xem.
    + Lưu lại được cookie đăng nhập để tránh đăng nhập quá nhiều lần, bị chặn IP.
    + Tự động hóa trong việc di chuột qua các tọa độ trên đồ thị để hiển thị dữ liệu và lấy nó về( bởi khi dữ liẹu hiển thị ra thì thẻ element tương ứng mới hiện để ta tìm và lấy được).( Khó )
    + Sử dụng được các phương thức trong Selenium để tìm các thẻ và lấy nội dung trong đó.
Bước 2:
  - Viết Script vào Console để tạo tool lấy tọa độ khi di chuột trên đồ thị
     function getMousePosition(canvas, event) {
            let rect = canvas.getBoundingClientRect();
            let x = event.clientX - rect.left;
            let y = event.clientY - rect.top;
            console.log("Coordinate x: " + x,
                "Coordinate y: " + y);
        }
 
        let canvasElem = document.querySelector("canvas");
 
        canvasElem.addEventListener("mousedown", function (e) {
            getMousePosition(canvasElem, e);
        }); 
