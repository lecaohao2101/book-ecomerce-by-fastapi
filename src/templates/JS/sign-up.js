var cities = [
  { country: 'Việt Nam', city: 'An Giang' },
  { country: 'Việt Nam', city: 'Bà Rịa - Vũng Tàu' },
  { country: 'Việt Nam', city: 'Bạc Liêu' },
  { country: 'Việt Nam', city: 'Bắc Giang' },
  { country: 'Việt Nam', city: 'Bắc Kạn' },
  { country: 'Việt Nam', city: 'Bắc Ninh' },
  { country: 'Việt Nam', city: 'Bến Tre' },
  { country: 'Việt Nam', city: 'Bình Định' },
  { country: 'Việt Nam', city: 'Bình Dương' },
  { country: 'Việt Nam', city: 'Bình Phước' },
  { country: 'Việt Nam', city: 'Bình Thuận' },
  { country: 'Việt Nam', city: 'Cà Mau' },
  { country: 'Việt Nam', city: 'Cần Thơ' },
  { country: 'Việt Nam', city: 'Cao Bằng' },
  { country: 'Việt Nam', city: 'Đà Nẵng' },
  { country: 'Việt Nam', city: 'Đắk Lắk' },
  { country: 'Việt Nam', city: 'Đắk Nông' },
  { country: 'Việt Nam', city: 'Điện Biên' },
  { country: 'Việt Nam', city: 'Đồng Nai' },
  { country: 'Việt Nam', city: 'Đồng Tháp' },
  { country: 'Việt Nam', city: 'Gia Lai' },
  { country: 'Việt Nam', city: 'Hà Giang' },
  { country: 'Việt Nam', city: 'Hà Nam' },
  { country: 'Việt Nam', city: 'Hà Nội' },
  { country: 'Việt Nam', city: 'Hà Tĩnh' },
  { country: 'Việt Nam', city: 'Hải Dương' },
  { country: 'Việt Nam', city: 'Hải Phòng' },
  { country: 'Việt Nam', city: 'Hậu Giang' },
  { country: 'Việt Nam', city: 'Hòa Bình' },
  { country: 'Việt Nam', city: 'Hồ Chí Minh' },
  { country: 'Việt Nam', city: 'Hưng Yên' },
  { country: 'Việt Nam', city: 'Khánh Hòa' },
  { country: 'Việt Nam', city: 'Kiên Giang' },
  { country: 'Việt Nam', city: 'Kon Tum' },
  { country: 'Việt Nam', city: 'Lai Châu' },
  { country: 'Việt Nam', city: 'Lâm Đồng' },
  { country: 'Việt Nam', city: 'Lạng Sơn' },
  { country: 'Việt Nam', city: 'Lào Cai' },
  { country: 'Việt Nam', city: 'Long An' },
  { country: 'Việt Nam', city: 'Nam Định' },
  { country: 'Việt Nam', city: 'Nghệ An' },
  { country: 'Việt Nam', city: 'Ninh Bình' },
  { country: 'Việt Nam', city: 'Ninh Thuận' },
  { country: 'Việt Nam', city: 'Phú Thọ' },
  { country: 'Việt Nam', city: 'Phú Yên' },
  { country: 'Việt Nam', city: 'Quảng Bình' },
  { country: 'Việt Nam', city: 'Quảng Nam' },
  { country: 'Việt Nam', city: 'Quảng Ngãi' },
  { country: 'Việt Nam', city: 'Quảng Ninh' },
  { country: 'Việt Nam', city: 'Quảng Trị' },
  { country: 'Việt Nam', city: 'Sóc Trăng' },
  { country: 'Việt Nam', city: 'Sơn La' },
  { country: 'Việt Nam', city: 'Tây Ninh' },
  { country: 'Việt Nam', city: 'Thái Bình' },
  { country: 'Việt Nam', city: 'Thái Nguyên' },
  { country: 'Việt Nam', city: 'Thanh Hóa' },
  { country: 'Việt Nam', city: 'Thừa Thiên Huế' },
  { country: 'Việt Nam', city: 'Tiền Giang' },
  { country: 'Việt Nam', city: 'Trà Vinh' },
  { country: 'Việt Nam', city: 'Tuyên Quang' },
  { country: 'Việt Nam', city: 'Vĩnh Long' },
  { country: 'Việt Nam', city: 'Vĩnh Phúc' },
  { country: 'Việt Nam', city: 'Yên Bái' }
];

// Lấy tham chiếu đến phần tử select quốc gia và thành phố
var countrySelect = document.getElementById('country');
var citySelect = document.getElementById('city');

// Lắng nghe sự kiện change của phần tử select quốc gia
countrySelect.addEventListener('change', function() {
  // Xóa tất cả các tùy chọn hiện có của phần tử select thành phố
  while (citySelect.firstChild) {
    citySelect.removeChild(citySelect.firstChild);
  }

  // Lấy tất cả các thành phố của quốc gia được chọn
  var selectedCountry = countrySelect.value;
  var matchingCities = cities.filter(function(city) {
    return city.country === selectedCountry;
  });

  // Tạo tùy chọn cho các thành phố được tìm thấy
  matchingCities.forEach(function(city) {
    var option = document.createElement('option');
    option.value = city.city;
    option.text = city.city;
    citySelect.appendChild(option);
  });
});
