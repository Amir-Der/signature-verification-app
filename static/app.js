// static/app.js
document.addEventListener('DOMContentLoaded', () => {
     const form = document.getElementById('upload-form');
     const resultDiv = document.getElementById('result');
     const previewDiv = document.getElementById('preview');
     const fileInput = document.getElementById('file-input');
     const submitBtn = document.getElementById('submit-btn');
   
     form.addEventListener('submit', async (e) => {
       e.preventDefault();
       resultDiv.classList.remove('show');
   
       const formData = new FormData(form);
       submitBtn.disabled = true;
       submitBtn.innerText = 'در حال بررسی... ⏳';
   
       try {
         const response = await fetch('/', { method: 'POST', body: formData });
         if (response.ok) {
           const data = await response.json();
           resultDiv.textContent = data.result;
         } else {
           resultDiv.textContent = 'خطا در پردازش تصویر';
         }
       } catch (err) {
         resultDiv.textContent = 'خطای شبکه';
       }
   
       resultDiv.classList.add('show');
       submitBtn.disabled = false;
       submitBtn.innerText = 'بررسی امضا';
     });
   
     fileInput.addEventListener('change', () => {
       const file = fileInput.files[0];
       previewDiv.innerHTML = '';
       if (file) {
         const reader = new FileReader();
         reader.onload = (e) => {
           previewDiv.innerHTML = `<img src="${e.target.result}" alt="پیش‌نمایش امضا">`;
         };
         reader.readAsDataURL(file);
       }
     });
   });
   