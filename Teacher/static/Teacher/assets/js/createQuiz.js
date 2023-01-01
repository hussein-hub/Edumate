
// let questions = [
//     {
//     numb: 1,
//     question: "What does HTML stand for?",
//     answer: "Hyper Text Markup Language",
//     options: [
//       "Hyper Text Preprocessor",
//       "Hyper Text Markup Language",
//       "Hyper Text Multiple Language",
//       "Hyper Tool Multi Language"
//     ]
//   },
//     {
//     numb: 2,
//     question: "What does CSS stand for?",
//     answer: "Cascading Style Sheet",
//     options: [
//       "Common Style Sheet",
//       "Colorful Style Sheet",
//       "Computer Style Sheet",
//       "Cascading Style Sheet"
//     ]
//   },
//     {
//     numb: 3,
//     question: "What does PHP stand for?",
//     answer: "Hypertext Preprocessor",
//     options: [
//       "Hypertext Preprocessor",
//       "Hypertext Programming",
//       "Hypertext Preprogramming",
//       "Hometext Preprocessor"
//     ]
//   },
//     {
//     numb: 4,
//     question: "What does SQL stand for?",
//     answer: "Structured Query Language",
//     options: [
//       "Stylish Question Language",
//       "Stylesheet Query Language",
//       "Statement Question Language",
//       "Structured Query Language"
//     ]
//   },
//     {
//     numb: 5,
//     question: "What does XML stand for?",
//     answer: "eXtensible Markup Language",
//     options: [
//       "eXtensible Markup Language",
//       "eXecutable Multiple Language",
//       "eXTra Multi-Program Language",
//       "eXamine Multiple Language"
//     ]
//   },
  

//      {
//      numb: 6,
//      question: "Your Question is Here",
  
//      options: [
//        "Option 1",
//        "option 2",
//        "option 3",
//        "option 4"
//     ]
//    },
// ];
// //selecting all required elements
// const start_btn = document.querySelector(".start_btn button");
// const info_box = document.querySelector(".info_box");
// const exit_btn = info_box.querySelector(".buttons .quit");
// const continue_btn = info_box.querySelector(".buttons .restart");
// const quiz_box = document.querySelector(".quiz_box");
// const result_box = document.querySelector(".result_box");
// const option_list = document.querySelector(".option_list");
// const time_line = document.querySelector("header .time_line");
// const timeText = document.querySelector(".timer .time_left_txt");
// const timeCount = document.querySelector(".timer .timer_sec");

// // if startQuiz button clicked
// start_btn.onclick = ()=>{
//     info_box.classList.add("activeInfo"); //show info box
// }

// // if exitQuiz button clicked
// exit_btn.onclick = ()=>{
//     info_box.classList.remove("activeInfo"); //hide info box
// }

// // if continueQuiz button clicked
// continue_btn.onclick = ()=>{
//     info_box.classList.remove("activeInfo"); //hide info box
//     quiz_box.classList.add("activeQuiz"); //show quiz box
//     showQuetions(0); //calling showQestions function
//     queCounter(1); //passing 1 parameter to queCounter
//     startTimer(15); //calling startTimer function
//     startTimerLine(0); //calling startTimerLine function
// }

// let timeValue =  15;
// let que_count = 0;
// let que_numb = 1;
// let userScore = 0;
// let counter;
// let counterLine;
// let widthValue = 0;

// const restart_quiz = result_box.querySelector(".buttons .restart");
// const quit_quiz = result_box.querySelector(".buttons .quit");

// // if restartQuiz button clicked
// restart_quiz.onclick = ()=>{
//     quiz_box.classList.add("activeQuiz"); //show quiz box
//     result_box.classList.remove("activeResult"); //hide result box
//     timeValue = 15; 
//     que_count = 0;
//     que_numb = 1;
//     userScore = 0;
//     widthValue = 0;
//     showQuetions(que_count); //calling showQestions function
//     queCounter(que_numb); //passing que_numb value to queCounter
//     clearInterval(counter); //clear counter
//     clearInterval(counterLine); //clear counterLine
//     startTimer(timeValue); //calling startTimer function
//     startTimerLine(widthValue); //calling startTimerLine function
//     timeText.textContent = "Time Left"; //change the text of timeText to Time Left
//     next_btn.classList.remove("show"); //hide the next button
// }

// // if quitQuiz button clicked
// quit_quiz.onclick = ()=>{
//     window.location.reload(); //reload the current window
// }

// const next_btn = document.querySelector("footer .next_btn");
// const bottom_ques_counter = document.querySelector("footer .total_que");

// // if Next Que button clicked
// next_btn.onclick = ()=>{
//     if(que_count < questions.length - 1){ //if question count is less than total question length
//         que_count++; //increment the que_count value
//         que_numb++; //increment the que_numb value
//         showQuetions(que_count); //calling showQestions function
//         queCounter(que_numb); //passing que_numb value to queCounter
//         clearInterval(counter); //clear counter
//         clearInterval(counterLine); //clear counterLine
//         startTimer(timeValue); //calling startTimer function
//         startTimerLine(widthValue); //calling startTimerLine function
//         timeText.textContent = "Time Left"; //change the timeText to Time Left
//         next_btn.classList.remove("show"); //hide the next button
//     }else{
//         clearInterval(counter); //clear counter
//         clearInterval(counterLine); //clear counterLine
//         showResult(); //calling showResult function
//     }
// }

// // getting questions and options from array
// function showQuetions(index){
//     const que_text = document.querySelector(".que_text");

//     //creating a new span and div tag for question and option and passing the value using array index
//     let que_tag = '<span>'+ questions[index].numb + ". " + questions[index].question +'</span>';
//     let option_tag = '<div class="option"><span>'+ questions[index].options[0] +'</span></div>'
//     + '<div class="option"><span>'+ questions[index].options[1] +'</span></div>'
//     + '<div class="option"><span>'+ questions[index].options[2] +'</span></div>'
//     + '<div class="option"><span>'+ questions[index].options[3] +'</span></div>';
//     que_text.innerHTML = que_tag; //adding new span tag inside que_tag
//     option_list.innerHTML = option_tag; //adding new div tag inside option_tag
    
//     const option = option_list.querySelectorAll(".option");

//     // set onclick attribute to all available options
//     for(i=0; i < option.length; i++){
//         option[i].setAttribute("onclick", "optionSelected(this)");
//     }
// }
// // creating the new div tags which for icons
// let tickIconTag = '<div class="icon tick"><i class="fas fa-check"></i></div>';
// let crossIconTag = '<div class="icon cross"><i class="fas fa-times"></i></div>';

// //if user clicked on option
// function optionSelected(answer){
//     clearInterval(counter); //clear counter
//     clearInterval(counterLine); //clear counterLine
//     let userAns = answer.textContent; //getting user selected option
//     let correcAns = questions[que_count].answer; //getting correct answer from array
//     const allOptions = option_list.children.length; //getting all option items
    
//     if(userAns == correcAns){ //if user selected option is equal to array's correct answer
//         userScore += 1; //upgrading score value with 1
//         answer.classList.add("correct"); //adding green color to correct selected option
//         answer.insertAdjacentHTML("beforeend", tickIconTag); //adding tick icon to correct selected option
//         console.log("Correct Answer");
//         console.log("Your correct answers = " + userScore);
//     }else{
//         answer.classList.add("incorrect"); //adding red color to correct selected option
//         answer.insertAdjacentHTML("beforeend", crossIconTag); //adding cross icon to correct selected option
//         console.log("Wrong Answer");

//         for(i=0; i < allOptions; i++){
//             if(option_list.children[i].textContent == correcAns){ //if there is an option which is matched to an array answer 
//                 option_list.children[i].setAttribute("class", "option correct"); //adding green color to matched option
//                 option_list.children[i].insertAdjacentHTML("beforeend", tickIconTag); //adding tick icon to matched option
//                 console.log("Auto selected correct answer.");
//             }
//         }
//     }
//     for(i=0; i < allOptions; i++){
//         option_list.children[i].classList.add("disabled"); //once user select an option then disabled all options
//     }
//     next_btn.classList.add("show"); //show the next button if user selected any option
// }

// function showResult(){
//     info_box.classList.remove("activeInfo"); //hide info box
//     quiz_box.classList.remove("activeQuiz"); //hide quiz box
//     result_box.classList.add("activeResult"); //show result box
//     const scoreText = result_box.querySelector(".score_text");
//     if (userScore > 3){ // if user scored more than 3
//         //creating a new span tag and passing the user score number and total question number
//         let scoreTag = '<span>and congrats! 🎉, You got <p>'+ userScore +'</p> out of <p>'+ questions.length +'</p></span>';
//         scoreText.innerHTML = scoreTag;  //adding new span tag inside score_Text
//     }
//     else if(userScore > 1){ // if user scored more than 1
//         let scoreTag = '<span>and nice 😎, You got <p>'+ userScore +'</p> out of <p>'+ questions.length +'</p></span>';
//         scoreText.innerHTML = scoreTag;
//     }
//     else{ // if user scored less than 1
//         let scoreTag = '<span>and sorry 😐, You got only <p>'+ userScore +'</p> out of <p>'+ questions.length +'</p></span>';
//         scoreText.innerHTML = scoreTag;
//     }
// }

// function startTimer(time){
//     counter = setInterval(timer, 1000);
//     function timer(){
//         timeCount.textContent = time; //changing the value of timeCount with time value
//         time--; //decrement the time value
//         if(time < 9){ //if timer is less than 9
//             let addZero = timeCount.textContent; 
//             timeCount.textContent = "0" + addZero; //add a 0 before time value
//         }
//         if(time < 0){ //if timer is less than 0
//             clearInterval(counter); //clear counter
//             timeText.textContent = "Time Off"; //change the time text to time off
//             const allOptions = option_list.children.length; //getting all option items
//             let correcAns = questions[que_count].answer; //getting correct answer from array
//             for(i=0; i < allOptions; i++){
//                 if(option_list.children[i].textContent == correcAns){ //if there is an option which is matched to an array answer
//                     option_list.children[i].setAttribute("class", "option correct"); //adding green color to matched option
//                     option_list.children[i].insertAdjacentHTML("beforeend", tickIconTag); //adding tick icon to matched option
//                     console.log("Time Off: Auto selected correct answer.");
//                 }
//             }
//             for(i=0; i < allOptions; i++){
//                 option_list.children[i].classList.add("disabled"); //once user select an option then disabled all options
//             }
//             next_btn.classList.add("show"); //show the next button if user selected any option
//         }
//     }
// }

// function startTimerLine(time){
//     counterLine = setInterval(timer, 29);
//     function timer(){
//         time += 1; //upgrading time value with 1
//         time_line.style.width = time + "px"; //increasing width of time_line with px by time value
//         if(time > 549){ //if time value is greater than 549
//             clearInterval(counterLine); //clear counterLine
//         }
//     }
// }

// function queCounter(index){
   
//     let totalQueCounTag = '<span><p>'+ index +'</p> of <p>'+ questions.length +'</p> Questions</span>';
//     bottom_ques_counter.innerHTML = totalQueCounTag;  
// }

var count = 1;
var radioCount = 2;
var totalRadioCount = 2;
var questionRadioCount = "";

function addOption() {
    // var parent = document.getElementsByClassName('Options');
    // console.log(parent);
    
    // const option = document.createElement('');
    // option.innerHTML = `
    //     <input class="form-control specialInputs" type="text" placeholder="Options" name="option">
    // `;
    radioCount++;
    totalRadioCount++;

    updateRadioCountOnForm(totalRadioCount);

    var individualOption = document.createElement('div');
    individualOption.setAttribute('class', 'individualOption');

    var option = document.createElement('input');
    option.setAttribute('class', 'form-control specialInputOptions');
    option.setAttribute('type', 'text');
    option.setAttribute('placeholder', 'Options');
    option.setAttribute('name', `option${count}`);

    var radioOption = document.createElement('input');
    radioOption.setAttribute('class', 'radioInput');
    radioOption.setAttribute('type', 'radio');
    radioOption.setAttribute('placeholder', 'Options');
    radioOption.setAttribute('name', `acoption${count}${radioCount}`);

    individualOption.appendChild(option);
    individualOption.appendChild(radioOption);


    var optionList = document.getElementsByClassName(`Options${count}`);
    // console.log(optionList);
    optionList[0].appendChild(individualOption);
    // var parent = optionList.parentNode;

    // ✅ Works
    // parent.appendChild(parent, optionList);
    // parent.insertBefore(option, optionList);
}

function addQuestion() {
    count++;
    questionRadioCount = questionRadioCount + String(radioCount);
    radioCount = 1;
    totalRadioCount++;
    updateCountOnForm(count);
    const questionDiv = document.createElement('div');
    questionDiv.setAttribute('class', 'single_question');
    // console.log(question);

    const question = document.createElement('input');
    question.setAttribute('class', 'form-control specialInputQuestions');
    question.setAttribute('type', 'text');
    question.setAttribute('placeholder', 'Question');
    question.setAttribute('name', `question${count}`);

    const optionList = document.createElement('div');
    optionList.setAttribute('class', `Options${count}`);
    
    var individualOption1 = document.createElement('div');
    individualOption1.setAttribute('class', 'individualOption');

    var individualOption2 = document.createElement('div');
    individualOption2.setAttribute('class', 'individualOption');

    const option1 = document.createElement('input');
    option1.setAttribute('class', 'form-control specialInputOptions');
    option1.setAttribute('type', 'text');
    option1.setAttribute('placeholder', 'Options');
    option1.setAttribute('name', `option${count}`);

    const radioOption1 = document.createElement('input');
    radioOption1.setAttribute('class', 'radioInput');
    radioOption1.setAttribute('type', 'radio');
    radioOption1.setAttribute('placeholder', 'Options');
    radioOption1.setAttribute('name', `acoption${count}${radioCount}`);
    radioCount++;
    totalRadioCount++;

    individualOption1.appendChild(option1);
    individualOption1.appendChild(radioOption1);

    const option2 = document.createElement('input');
    option2.setAttribute('class', 'form-control specialInputOptions');
    option2.setAttribute('type', 'text');
    option2.setAttribute('placeholder', 'Options');
    option2.setAttribute('name', `option${count}`);

    const radioOption2 = document.createElement('input');
    radioOption2.setAttribute('class', 'radioInput');
    radioOption2.setAttribute('type', 'radio');
    radioOption2.setAttribute('placeholder', 'Options');
    radioOption2.setAttribute('name', `acoption${count}${radioCount}`);

    individualOption2.appendChild(option2);
    individualOption2.appendChild(radioOption2);

    optionList.append(individualOption1);
    optionList.append(individualOption2);

    questionDiv.appendChild(question);
    questionDiv.appendChild(optionList);

    const addButton = document.getElementById('addOptions');
    // console.log(addButton);
    var parent = addButton.parentNode;

    // ✅ Works
    // parent.appendChild(parent, option);
    parent.insertBefore(questionDiv, addButton);
    updateRadioCountOnForm(totalRadioCount);
    rdc(questionRadioCount);
}

function updateCountOnForm(count) {
    var countKeeper = document.getElementById('QuestionCount');
    countKeeper.value = count; 
}

function updateRadioCountOnForm(totalRadioCount) {
    var countKeeper = document.getElementById('radioCount');
    countKeeper.value = totalRadioCount; 
}

function rdc(questionRadioCount) {
    var questionRadioCountString = document.getElementById('rdc');
    questionRadioCountString.value = questionRadioCount;

    console.log(questionRadioCount);
}

function updateAll() {
    questionRadioCount = questionRadioCount + String(radioCount);
    rdc(questionRadioCount);
}