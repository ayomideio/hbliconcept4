const date_picker = document.querySelector(".date-picker");
const  selected_date_element = document.querySelector(".selected-date");
const date_element = document.querySelector(".dates");
const month_element = document.querySelector(".mth");
const week_day_element = document.querySelector(".week_days");
const days_element = document.querySelector(".days");
// from Nodelist turned into array  
const buttons =[...document.querySelectorAll('.arrows')];


 
// find particular button in the buttonsDOM array
let buttonsDOM =[];
 buttonsDOM= buttons;



const months = ['january' , 'february' , 'march', 'april','may' ,'june' , 'july', 'august', 'september', 'october', 'november', 'december'];
const weekDays = [ 'sun', 'mon' , 'tue' , 'wed', 'thu','fri' ,'sat'];

/**  CURRENT DATE */
let date = new Date();
// - return current day
let day = date.getDate();
let month =date.getMonth();
let year =date.getFullYear();

let selectedDate= date;
let selectedDay= day;
let selectedMonth= month;
let selectedYear= year;

/** DISPLAY MONTH */
formatDate(date);
displayMonthElement(months,month , year);
displayWeekdayElement(day)
populateDays();

/** EVENT LISTENERS */
/** create toggle */
date_picker.addEventListener("click", toggleDatePicker);

buttons.forEach((button)=>{
   
    button.addEventListener('click', ()=>{

    button.classList.contains('prev-month') && getToPrevMonth();
    button.classList.contains('next-month') &&  getToNextMonth();

    populateDays();
    displayMonthElement(months,month , year);
    
    })
 });


/**  FUNCTIONS */
function  toggleDatePicker(e){
    // console.log(e.path);
    if(!checkEvenPathForClass(e.path, "dates")){
        date_element.classList.toggle("active");
    }
}

function getToPrevMonth(){
    // 1 - decrease month
    month--;
    // month start at 0=>january -- 11=>december
    if(month < 0){
        month=11;
        //decrease year
        year--;
    }
}

function getToNextMonth(){
    // 1 - increase month
    month++;
    // month start at 0=>january -- 11=>december
    if(month > 11){
        month=0;
        //increase year
        year++;
    }
}

function populateDays(){
    // gets the day of the week for this date
    let firstDay = new Date(year, month).getDay();
    
    // everytime we run this func we want to clear the current days in there - because when click next or prev we will rerender the days
    days_element.innerHTML = '';
    
    // checking the mount of days in this month to control the loop
    let totalDays = daysInMonth(month, year);

    // adding the blank boxes so that date start on correct day of the week
    blankDates(firstDay);
 
    for(let i= 0; i < totalDays; i++){
  
       const day_element = document.createElement('div');
 
       let day = i + 1;
 
       day_element.classList.add('day');
       day_element.textContent = day;
       
     ( selectedDay ===  day &&  selectedMonth ===month && selectedYear===year) && day_element.classList.add('selected');
  

        // change day when user click
        day_element.addEventListener('click', ()=>{
        //  Integer value representing the month, beginning with 0 for January to 11 for December.
        selectedDate= new Date(`${year}-${month+1}-${day}`);
        
        selectedDay= day;
        selectedMonth= month;
        selectedYear= year;
        
 
        formatDate(selectedDate);
        // when click on element recall
        populateDays();
       }); 
 
       days_element.appendChild( day_element);
    } 
}


/** HERLPER FUNCTIONS */
/*
 1- check where we click
    - where we click we get an event & this give us the path where we clicked
*/ 
 
 function checkEvenPathForClass(path,  selector){
     for(let i = 0; i < path.length; i++){
         if(path[i].classList && path[i].classList.contains(selector)){
            return true;
         }
     }
     return false;
 } 

 /* format month & year */ 

 function displayMonthElement(months,month , year){
   return month_element.textContent = `${months[month]} ${year}`
 } 

 function displayWeekdayElement(day){
     weekDays.forEach(d=>{
        const day_element = document.createElement('div');

        day_element.classList.add('day-name');
        day_element.textContent = d;
        week_day_element.appendChild( day_element);
     })

    //  Integer value representing the day of the month. If not specified, the default value of 1 is used
//    return week_day_element.textContent = `${weekDays+1[day]} `
 } 

 function daysInMonth(month, year) {
	// day 0 here returns the last day of the PREVIOUS month
	return new Date(year, month + 1, 0).getDate();
}



 function formatDate(day){
    let daySelected = day.getDate();
     // get current month of day we pass throught
    // month array from 0 (january) to 11 (december)
    let month = day.getMonth() + 1;

    daySelected < 10 && (daySelected = `0${daySelected}`);
    month < 10 && (month = `0${month}`);
   
    let year = day.getFullYear();

    // to get the value - the current day selected from the element
    selected_date_element.dataset.value = selectedDate;
     
    return selected_date_element.textContent = `${daySelected} / ${month} / ${year}`;
 }
 

 function blankDates(count) {
	// looping to add the correct amount of blank days to the calendar
	for (let x = 0; x < count; x++) {
        const day_element = document.createElement('div');

		let clearCell = document.createTextNode("");
		day_element.appendChild(clearCell);
        days_element.appendChild( day_element);
	}
}