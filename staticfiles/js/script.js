

 document.addEventListener("DOMContentLoaded", function() {
     const monthYearElement = document.getElementById('month-year');
     const calendarDaysElement = document.getElementById('calendar-days');
     const prevMonthBtn = document.getElementById('prev-month');
     const nextMonthBtn = document.getElementById('next-month');
     let currentDate = new Date();
     function renderCalendar(date) {
         const year = date.getFullYear();
         const month = date.getMonth();
         const firstDay = new Date(year, month, 1).getDay();
         const lastDate = new Date(year, month + 1, 0).getDate();
         const monthNames = [
             "January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"
         ];
         monthYearElement.textContent = `${monthNames[month]} ${year}`;
         let days = "";
         for (let i = 0; i < firstDay; i++) {
             days += "<td></td>";
         }
         for (let i = 1; i <= lastDate; i++) {
             const today = new Date();
             const isToday = i === today.getDate() &&
                             year === today.getFullYear() &&
                             month === today.getMonth();
             days += `<td class="${isToday ? 'today' : ''}">${i}</td>`;
             if ((i + firstDay) % 7 === 0) {
                 days += "</tr><tr>";
             }
         }
         calendarDaysElement.innerHTML = `<tr>${days}</tr>`;
     }
     renderCalendar(currentDate);
     prevMonthBtn.addEventListener('click', () => {
         currentDate.setMonth(currentDate.getMonth() - 1);
         renderCalendar(currentDate);
     });
     nextMonthBtn.addEventListener('click', () => {
         currentDate.setMonth(currentDate.getMonth() + 1);
         renderCalendar(currentDate);
     });
 });


//  create batch  Modal

document.addEventListener('DOMContentLoaded', function () {
    var createBatchModal = document.getElementById('createBatchModal');
    createBatchModal.addEventListener('hidden.bs.modal', function () {
        var form = createBatchModal.querySelector('form');
        form.reset(); 
    });
});