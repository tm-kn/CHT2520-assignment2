import setupDatePicker from '@components/datePicker';
import setupDeleteButton from '@components/deleteButton';
import setupNavBar from '@components/navBar';
import perProjectChart from '@components/perProjectChart';


document.addEventListener('DOMContentLoaded', () => {
    setupDatePicker();
    setupDeleteButton();
    setupNavBar();
    perProjectChart();
});
