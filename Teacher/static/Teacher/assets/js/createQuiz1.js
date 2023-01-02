var count = 1;
var radioCount = 2;
var totalRadioCount = 2;
var questionRadioCount = "2";
var totalQuestionCount = 1;

var questionRadioCountArray = [[1, 2]];

function addOption() {

    console.log("\nBEFORE UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);
    // var parent = document.getElementsByClassName('Options');
    // console.log(parent);
    
    // const option = document.createElement('');
    // option.innerHTML = `
    //     <input class="form-control specialInputs" type="text" placeholder="Options" name="option">
    // `;

    // questionRadioCount = questionRadioCount.slice(0,questionRadioCount.length-1) + String(parseInt(questionRadioCount[questionRadioCount.length-1]) + 1);

    var last = questionRadioCountArray.pop();
    var single = last.pop()
    single++;
    last.push(single);
    questionRadioCountArray.push(last);
    radioCount++;
    totalRadioCount++;

    updateRadioCountOnForm(totalRadioCount);

    var individualOption = document.createElement('div');
    individualOption.setAttribute('class', 'individualOption');

    var option = document.createElement('input');
    option.setAttribute('class', 'form-control specialInputOptions');
    option.setAttribute('type', 'text');
    option.setAttribute('placeholder', 'Options');
    option.setAttribute('name', `option${totalQuestionCount}`);

    var radioOption = document.createElement('input');
    radioOption.setAttribute('class', 'radioInput');
    radioOption.setAttribute('type', 'radio');
    radioOption.setAttribute('placeholder', 'Options');
    radioOption.setAttribute('name', `acoption${totalQuestionCount}${radioCount}`);

    individualOption.appendChild(option);
    individualOption.appendChild(radioOption);


    var optionList = document.getElementsByClassName(`Options${totalQuestionCount}`);
    // console.log(optionList);
    optionList[0].appendChild(individualOption);
    // var parent = optionList.parentNode;

    // ✅ Works
    // parent.appendChild(parent, optionList);
    // parent.insertBefore(option, optionList);

    console.log("AFTER UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);
}

function addQuestion() {

    console.log("\nBEFORE UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);

    // important check keeping LOC
    count++;
    totalQuestionCount++;
    radioCount = 1;
    totalRadioCount++;
    updateCountOnForm(count);




    const questionDiv = document.createElement('div');
    questionDiv.setAttribute('id', `sq${totalQuestionCount}`);
    questionDiv.setAttribute('class', `single_question${totalQuestionCount}`);
    // console.log(question);


    const individualQuestion = document.createElement('div');
    individualQuestion.setAttribute('class', 'individualQuestion');

    
    const question = document.createElement('input');
    question.setAttribute('class', 'form-control specialInputQuestions');
    question.setAttribute('type', 'text');
    question.setAttribute('placeholder', 'Question');
    question.setAttribute('name', `question${totalQuestionCount}`);

    const deleteButton = document.createElement('a');
    deleteButton.setAttribute('class', 'btn delete_button');
    deleteButton.setAttribute('id', `${totalQuestionCount}`);
    deleteButton.setAttribute('onclick', 'deleteQuestion(this.id)');

    const deleteIcon = document.createElement('i');
    deleteButton.setAttribute('class', 'fa fa-trash');
    
    deleteButton.appendChild(deleteIcon);

    individualQuestion.appendChild(question);
    individualQuestion.appendChild(deleteButton);


    const optionList = document.createElement('div');
    optionList.setAttribute('class', `Options${totalQuestionCount}`);
    
    var individualOption1 = document.createElement('div');
    individualOption1.setAttribute('class', 'individualOption');

    var individualOption2 = document.createElement('div');
    individualOption2.setAttribute('class', 'individualOption');

    const option1 = document.createElement('input');
    option1.setAttribute('class', 'form-control specialInputOptions');
    option1.setAttribute('type', 'text');
    option1.setAttribute('placeholder', 'Options');
    option1.setAttribute('name', `option${totalQuestionCount}`);

    const radioOption1 = document.createElement('input');
    radioOption1.setAttribute('class', 'radioInput');
    radioOption1.setAttribute('type', 'radio');
    radioOption1.setAttribute('placeholder', 'Options');
    radioOption1.setAttribute('name', `acoption${totalQuestionCount}${radioCount}`);
    radioCount++;
    totalRadioCount++;

    individualOption1.appendChild(option1);
    individualOption1.appendChild(radioOption1);

    const option2 = document.createElement('input');
    option2.setAttribute('class', 'form-control specialInputOptions');
    option2.setAttribute('type', 'text');
    option2.setAttribute('placeholder', 'Options');
    option2.setAttribute('name', `option${totalQuestionCount}`);

    const radioOption2 = document.createElement('input');
    radioOption2.setAttribute('class', 'radioInput');
    radioOption2.setAttribute('type', 'radio');
    radioOption2.setAttribute('placeholder', 'Options');
    radioOption2.setAttribute('name', `acoption${totalQuestionCount}${radioCount}`);

    individualOption2.appendChild(option2);
    individualOption2.appendChild(radioOption2);

    optionList.append(individualOption1);
    optionList.append(individualOption2);

    questionDiv.appendChild(individualQuestion);
    questionDiv.appendChild(optionList);

    const addButton = document.getElementById('addOptions');
    // console.log(addButton);
    var parent = addButton.parentNode;

    // ✅ Works
    // parent.appendChild(parent, option);
    parent.insertBefore(questionDiv, addButton);
    updateRadioCountOnForm(totalRadioCount);
    




    questionRadioCountArray.push([totalQuestionCount, radioCount]);

    // questionRadioCount = questionRadioCount + String(radioCount);
    rdc(questionRadioCountArray);
    
    console.log("AFTER UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);
}

function updateCountOnForm(count) {
    var countKeeper = document.getElementById('QuestionCount');
    countKeeper.value = count; 
}

function updateRadioCountOnForm(totalRadioCount) {
    var countKeeper = document.getElementById('radioCount');
    countKeeper.value = totalRadioCount; 
}

function rdc(questionRadioCountArray) {
    var questionRadioCountString = document.getElementById('rdc');
    questionRadioCountString.value = questionRadioCountArray;

    // console.log(questionRadioCount);
}

// function updateAll() {
//     questionRadioCount = questionRadioCount + String(radioCount);
//     rdc(questionRadioCount);
// }

function deleteQuestion(questionID) {
    console.log("\nBEFORE UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);
    var classNameOfQuestionToRemove = "sq" + questionID;
    const element = document.getElementById(classNameOfQuestionToRemove);
    // console.log(element);
    element.remove();
    count--;
    updateCountOnForm(count);
    totalRadioCount = totalRadioCount - radioCount;
    updateRadioCountOnForm(totalRadioCount);
    // console.log(radioCount);
    questionID = parseInt(questionID);


    /* 
    questionRadioCountArray = [[1, 2], [2, 4], [3, 2]]
    
    */
    var double = questionRadioCountArray.pop();
    radioCount = double.pop();
    double.push(radioCount);
    questionRadioCountArray.push(double);

    var firstArray = [];
    for (var i = 0; i < questionRadioCountArray.length; i++) {
        firstArray.push(questionRadioCountArray[i][0]);
    }    
    console.log(firstArray);
    var index = firstArray.indexOf(questionID);
    questionRadioCountArray.splice(index, 1);


    // radioCount = parseInt(questionRadioCount[questionRadioCount.length-1]);
    // questionRadioCount = questionRadioCount.slice(0,questionID) + questionRadioCount.slice(questionID+1,);
    // console.log(questionRadioCount);
    rdc(questionRadioCountArray);

    console.log("AFTER UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);
}