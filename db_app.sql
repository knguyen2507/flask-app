CREATE DATABASE db_app
GO

USE db_app
GO

---------------------------------------------------------------------------------------------------------------------------------------------------------------------
--function

CREATE FUNCTION autoID()
RETURNS NVARCHAR(8)
AS
	BEGIN
		DECLARE @c INT
		DECLARE @id NVARCHAR(8)
		SELECT @c = COUNT(id_user)+1 FROM user_app
		SELECT @id = CASE
			WHEN @c >= 0 AND @c < 10 THEN 'user00' + CONVERT(CHAR(3),@c)
			WHEN @c >= 10 AND @c < 100 THEN 'user0' + CONVERT(CHAR(3),@c)
			ELSE 'user' + CONVERT(CHAR,@c)
		END
		RETURN @id
	END
GO

---------------------------------------------------------------------------------------------------------------------------------------------------------------------
--create table

CREATE TABLE user_app
(
	id_user NVARCHAR(10) NOT NULL PRIMARY KEY DEFAULT dbo.autoID(),
	name_user NVARCHAR(40),
	phone_user NVARCHAR(10)
)

CREATE TABLE user_login
(
	us NVARCHAR(10),
	pw NVARCHAR(255),
	id_user NVARCHAR(10) NOT NULL FOREIGN KEY (id_user) REFERENCES user_app(id_user) ON UPDATE CASCADE,
	roll INT
	PRIMARY KEY(id_user)
)
GO

CREATE TABLE category
(
	id_cate NVARCHAR(10) NOT NULL PRIMARY KEY,
	name_cate NVARCHAR(40),
	image_cate NVARCHAR(50)
)
GO

CREATE TABLE brand
(
	id_brand NVARCHAR(10) NOT NULL PRIMARY KEY,
	name_brand NVARCHAR(40),
	logo_brand NVARCHAR(50)
)
GO

CREATE TABLE product
(
	id_prod NVARCHAR(10) NOT NULL PRIMARY KEY,
	name_prod NVARCHAR(40),
	image_prod NVARCHAR(50),
	lis_image_prod NVARCHAR(50),
	des_prod NVARCHAR(500),
	id_cate NVARCHAR(10) NOT NULL FOREIGN KEY (id_cate) REFERENCES category(id_cate) ON DELETE CASCADE,
	amount_prod INT,
	price_prod NVARCHAR(10),
	id_brand NVARCHAR(10) FOREIGN KEY (id_brand) REFERENCES brand(id_brand) ON DELETE CASCADE
)
GO
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
--insert user

INSERT INTO dbo.user_app
(
	id_user, name_user, phone_user
) 
VALUES
(
	'user001', 'Admin', '0123456789'
)

INSERT INTO dbo.user_app
(
	id_user, name_user, phone_user
) 
VALUES
(
	'user002', N'Nguyên Phát', '0123456789'
)

INSERT INTO dbo.user_app
(
	id_user, name_user, phone_user
) 
VALUES
(
	'user003', N'Nguyễn Văn A', '0123456789'
)

INSERT INTO dbo.user_app
(
	id_user, name_user, phone_user
) 
VALUES
(
	'user004', N'Trần Thị B', '0123456789'
)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

INSERT INTO dbo.user_login
(
	us, pw, id_user, roll
) 
VALUES
(
	'admin', 'e10adc3949ba59abbe56e057f20f883e', 'user001', '0'
)

INSERT INTO dbo.user_login
(
	us, pw, id_user, roll
) 
VALUES
(
	'np', 'e10adc3949ba59abbe56e057f20f883e', 'user002', '1'
)

INSERT INTO dbo.user_login
(
	us, pw, id_user, roll
) 
VALUES
(
	'vana', 'e10adc3949ba59abbe56e057f20f883e', 'user003', '2'
)

INSERT INTO dbo.user_login
(
	us, pw, id_user, roll
) 
VALUES
(
	'thib', 'e10adc3949ba59abbe56e057f20f883e', 'user004', '2'
)
GO
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
--insert category

INSERT INTO dbo.category
(
	id_cate, name_cate, image_cate
) 
VALUES
(
	'banghe', N'đồ gỗ', 'static/images/category/ban-ghe-go.png'
)

INSERT INTO dbo.category
(
	id_cate, name_cate, image_cate
) 
VALUES
(
	'locnuoc', N'máy lọc nước', 'static/images/category/may-loc-nuoc.png'
)

INSERT INTO dbo.category
(
	id_cate, name_cate, image_cate
) 
VALUES
(
	'tulanh', N'tủ lạnh', 'static/images/category/tu-lanh.png'
)

INSERT INTO dbo.category
(
	id_cate, name_cate, image_cate
) 
VALUES
(
	'maygiat', N'máy giặt', 'static/images/category/may-giat.png'
)

INSERT INTO dbo.category
(
	id_cate, name_cate, image_cate
) 
VALUES
(
	'tv', N'smart tv', 'static/images/category/tv.png'
)

INSERT INTO dbo.category
(
	id_cate, name_cate, image_cate
) 
VALUES
(
	'quat', N'quạt', 'static/images/category/quat.png'
)

INSERT INTO dbo.category
(
	id_cate, name_cate, image_cate
) 
VALUES
(
	'noithat', N'đồ nội thất', 'static/images/category/noi-that.png'
)

INSERT INTO dbo.category
(
	id_cate, name_cate, image_cate
) 
VALUES
(
	'giadung', N'đồ gia dụng', 'static/images/category/gia-dung.png'
)

INSERT INTO dbo.category
(
	id_cate, name_cate, image_cate
) 
VALUES
(
	'nem', N'nệm', 'static/images/category/nem.png'
)
GO

---------------------------------------------------------------------------------------------------------------------------------------------------------------------
--insert brand

INSERT INTO dbo.brand
(
	id_brand, name_brand, logo_brand
) 
VALUES
(
	'mutosi', N'Mutosi', 'static/images/brand/mutosi.png'
)

INSERT INTO dbo.brand
(
	id_brand, name_brand, logo_brand
) 
VALUES
(
	'toshiba', N'Toshiba', 'static/images/brand/toshiba.png'
)

INSERT INTO dbo.brand
(
	id_brand, name_brand, logo_brand
) 
VALUES
(
	'samsung', N'Samsung', 'static/images/brand/samsung.png'
)

INSERT INTO dbo.brand
(
	id_brand, name_brand, logo_brand
) 
VALUES
(
	'hitachi', N'Hitachi', 'static/images/brand/hitachi.png'
)

INSERT INTO dbo.brand
(
	id_brand, name_brand, logo_brand
) 
VALUES
(
	'sunhouse', N'SunHouse', 'static/images/brand/sunhouse.png'
)

INSERT INTO dbo.brand
(
	id_brand, name_brand, logo_brand
) 
VALUES
(
	'panasonic', N'Panasonic', 'static/images/brand/panasonic.png'
)

INSERT INTO dbo.brand
(
	id_brand, name_brand, logo_brand
) 
VALUES
(
	'lg', N'LG', 'static/images/brand/lg.png'
)

INSERT INTO dbo.brand
(
	id_brand, name_brand, logo_brand
) 
VALUES
(
	'sony', N'Sony', 'static/images/brand/sony.png'
)

INSERT INTO dbo.brand
(
	id_brand, name_brand, logo_brand
) 
VALUES
(
	'apechome', N'ApecHome', 'static/images/brand/apechome.png'
)

INSERT INTO dbo.brand
(
	id_brand, name_brand, logo_brand
) 
VALUES
(
	'khac', N'Khác', ''
)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------
--insert product

INSERT INTO dbo.product
(
	id_prod, name_prod, image_prod, lis_image_prod, des_prod, id_cate, amount_prod, price_prod, id_brand
)
VALUES
(
	'gr-rb405we', 'Tủ Lạnh Toshiba Inverter GR-RB405WE', 'static/images/product/gr-rb405we/gr-rb405we_1.png', 'static/images/product/gr-rb405we', '', 'tulanh', '2', '17000000', 'toshiba' 
)