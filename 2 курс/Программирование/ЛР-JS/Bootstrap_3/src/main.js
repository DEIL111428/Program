import './styles.scss';

import { Modal } from 'bootstrap';

// Импорт Luxon
import { DateTime } from 'luxon';

// Логика обновления времени при открытии
const timeModal = document.getElementById('timeModal');

if (timeModal) {
  timeModal.addEventListener('show.bs.modal', function () {
    // Получаем текущее время через Luxon
    const now = DateTime.now()
        .setLocale('ru')
        .toLocaleString(DateTime.DATETIME_FULL);
    
    // Вставляем в DOM
    const dateContainer = document.getElementById('currentDateTime');
    if(dateContainer) {
        dateContainer.textContent = now;
    }
  });
}