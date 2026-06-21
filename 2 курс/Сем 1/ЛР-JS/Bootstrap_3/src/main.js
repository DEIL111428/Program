import './styles.scss';

import Modal from 'bootstrap/js/dist/modal';

// Импорт Luxon
import { DateTime } from 'luxon';

// Логика обновления времени при открытии
const timeModal = document.getElementById('timeModal');
let timeInterval;

function updateTime() {
  const dateContainer = document.getElementById('currentDateTime');
  if (dateContainer) {
    dateContainer.textContent = DateTime.now()
      .setLocale('ru')
      .toLocaleString(DateTime.DATETIME_FULL_WITH_SECONDS || DateTime.DATETIME_FULL);
  }
}

if (timeModal) {
  timeModal.addEventListener('show.bs.modal', function () {
    updateTime(); // Устанавливаем время сразу при открытии
    timeInterval = setInterval(updateTime, 1000); // Обновляем каждую секунду
  });

  timeModal.addEventListener('hide.bs.modal', function () {
    if (timeInterval) {
      clearInterval(timeInterval); // Очищаем интервал при закрытии
    }
  });
}