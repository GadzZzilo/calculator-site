document.addEventListener('DOMContentLoaded', function() {
  const inputField = document.getElementById('inputField'); // Получение элемента строки ввода
  const keyboardButtons = document.querySelectorAll('.btn btn-outline-primary'); // Получение всех кнопок клавиатуры

  keyboardButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      inputField.value += button.textContent; // Добавление текста кнопки в конец строки ввода
    });
  });
});