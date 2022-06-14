# Özet

Bu uygulamada amaç adminden tarafından önceden belirlenen sorulara göre
verilen süre boyunca kullanıcıdan görüntü ve ses verisi alıp sunucuya kaydedilmesidir.

# Kurulum

## Sanal Çevre Kurulumu (virtualenv)

Proje kaynak kodunun koşturulabilmesi için gereken kütüphaneler sanal ortama kurulmalıdır.
Sanal ortam oluşturmak için virtualenv kütüphanesi kullanılabilir.

```
pip install virtualenv
```

Sanal ortam kurulumu için

```
virtualenv venv
```

komutu koşturularak "venv" ismi ile bir ortam oluşturulur.

## Ortamın Aktive Edilmesi

Ortamı aktif etmek için Windows işletim sisteminde

```
venv\Scripts\activate.bat
```

Linux işletim sistemi için

```
source venv/bin/activate
```

komutu koşturulur.

## Kütüphaneleri Yüklenmesi

İlgili kütüphaneleri yüklemek için

```
pip install -r requirements.txt
```

komutu koşturulur.

## Sunucunun Ayağa Kaldırılması

Projeyi ayağa kaldırmak için

```
python manage.py runserver
```

komutu koşturulur.
Bu komutu koşturmadan önce kurulan sanal ortamın aktif olduğundan ve proje dizininde bulunulduğundan emin olunmalıdır.

# Proje Mimarisi

```
project
│
└─── apps                               -- Django framework kapsamında üretilen uygulamaların bulunduğu klasör
│    │
│    └─── common                        -- Diğer projelerde kullanılabilecek yardımcı fonksiyon ve sınıfların bulunduğu klasör
│    └─── opencvdjango                  -- Projenin ana uygulaması
│          │           
│          └─── models.py               -- Veritabanı modellerinin bulunduğu script dosyası
│          └─── urls.py                 -- Uygulamadaki endpointler ile python view fonksiyonlarının eşleştirildiği script dosyası
│          └─── views.py                -- Uygulamadaki sayfaların gösterilmesi ve video kaydının gerçekleştirildiği script dosyası
│
└─── core                               -- Uygulamanın asıl ayarlarının bulunduğu klasör
│
└─── mediafiles                         -- Sunucu tarafından kaydedilen videoların bulunduğu klasör
│
└─── staticfiles                        -- Sunucudaki static dosyaların (css, javascript, fonts vb) bulunduğu klasör
│    │
│    └─── css                           
│    └─── fonts                          
│    └─── js                            
│
└─── templates                          -- html uzantılı dosyaların bulunduğu klasör
│
│   README.md                           -- Uygulama dökümanasyonunun bulunduğu dosya
│   requirements.txt                    -- Gerekli kütüphaneleri belirtildiği dosya
│   manage.py                           -- Sunucuyu ayağa kaldırma vs gibi yardımcı fonksiyonları barındıran ana script
│   .gitignore                          -- git tarafından takip edilmemesi istenen dosya ve klasörlerin belirtildiği dosya
```

# Modeller

## UserEntry

UserEntry modeli kullanıcıya sorulacak soruları temsil eder.

```
class UserEntry(AuditMixin):

    header = models.CharField(max_length=600)
    description = models.TextField(max_length=1500)
    created_date = models.DateTimeField(auto_now_add=True)
    video_time = models.IntegerField(default=00, verbose_name="Video Süresi Dakika: ",
                                     validators=[MinValueValidator(0), MaxValueValidator(60)])
    video_sec = models.IntegerField(default=00, verbose_name="Video Süresi Saniye: ",
                                    validators=[MinValueValidator(0), MaxValueValidator(60)])

    def __str__(self) -> str:
        return f"{self.header}"

    class Meta:
        verbose_name = "Soru Girişi"
        verbose_name_plural = "Soru Girişleri"
        ordering = ["id"]

```

## UserAnswer

UserAnswer modeli kullanıcıyı sorulan sorular sonucunda verdiği cevapları temsil eder.

```
class UserAnswer(AuditMixin):
    header = models.CharField(max_length=50)
    doc = models.FileField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.header}"
```

# Uç Noktalar

Uygulamada 2 ana uç nokta bulunmaktadır.

* ``/`` uç noktası soruların gösterildiği uç noktadır.
* ``/upload/`` uç noktası videonun kullanıcı tarafından POST isteğinin gönderildiği uç noktadır.

```
urlpatterns = [
    path('', index, name='index'),
    path('upload/', views.upload_file),
 ]
```

# Bazı Önemli Fonksiyonlar

## Soru sayfalarının gösterilmesi

Sorular kullanıcıya gösterilirken _page_ query sine göre sayfa gösterilir.
Eğer _page_ query si bulunmuyorsa birinci sorudan sorular sorulmaya başlar.
_page_ query si bulunuyor ise ilk başta query nin doğruluğu kontrol edilir.
Eğer istenilen formatta gelmemiş ise hata sayfası gösterilir.

```
def index(request):
    context = {}
    filtered_quiz = UserEntry.objects.all()
    paginator = Paginator(filtered_quiz, 1)

    page_number: str | None | int = request.GET.get('page')

    if page_number is None:
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
        return render(request, "index.html", context)

    if isinstance(page_number, str) and page_number.isdigit():
        page_obj = paginator.get_page(page_number)
        page_number = int(page_number)
        if page_number > paginator.num_pages:
            print("page number out of range ")
            return render(request, "endOfTest.html")
        context['object_list'] = page_obj
        return render(request, "index.html", context)

    return render(request, "error.html", context)

```

## Videonun kullanıcıdan Sunucuya Gönderilmesi

Video tarayıcı yardımı ile kaydedildikten sonra sunucuya POST isteği yollayarak ilgili verileri gönderir.
Gönderme işlemi başarılı olduktan sonra kullanıcı bilgilendirilir ve diğer soruya geçiş yapılı.
Eğer bütün sorular çözülmüşse _Test Bitti_ sayfasına kullanıcı yönlendirilir.

```
$.ajax({
    method: "POST",
    url: "/upload/",
    processData: false,
    contentType: false,
    cache: false,
    mimeType: "multipart/form-data",
    data: data,
    wait: true,
    success: function (res) {
        alert("Kayıt başarılı bir şekilde gönderildi", res);
        const params = new URLSearchParams(window.location.search)
        let page_number = params.has("page") ? parseInt(params.get("page")) : 1
        window.location.href = `?page=${page_number + 1}`
    },
})
```

## Videoların Veritabanına Kaydedilmesi

Kullanıcı tarafından gönderilen POST isteği ile veritabanında yeni bir _cevap_ girdisi oluşturulur ve veritabanına
kaydedilir.

```
def upload_file(request):
    file = request.FILES.get('file')
    print("file.name", file.name, "file.size", file.size)

    UserAnswer.objects.create(header=file, doc=file)

    return JsonResponse({"file": file.name, "size": file.size})
```

# Hata Ayıklama

Geliştirme aşamasında test amaçlı admin hesabı oluşturulmuştur.

* Kullanıcı adı => ``test``
* Şifre => ``123``

