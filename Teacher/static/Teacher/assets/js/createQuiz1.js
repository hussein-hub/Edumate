var count = 1;
var radioCount = 2;
var totalRadioCount = 2;
var questionRadioCount = "2";
var totalQuestionCount = 1;
var latestQuestionID = 1;

// [sq#, radioCount]
var questionRadioCountArray = [[1, 2]];

function addOption() {

    console.log("\nBEFORE UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);
    console.log("Latest QuestionID : " + latestQuestionID);

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
    option.setAttribute('name', `option${latestQuestionID}`);

    var radioOption = document.createElement('input');
    radioOption.setAttribute('class', 'radioInput');
    radioOption.setAttribute('type', 'checkbox');
    radioOption.setAttribute('placeholder', 'Options');
    radioOption.setAttribute('name', `acoption${latestQuestionID}${radioCount}`);

    individualOption.appendChild(option);
    individualOption.appendChild(radioOption);


    var optionList = document.getElementsByClassName(`Options${latestQuestionID}`);
    optionList[0].appendChild(individualOption);
    // var parent = optionList.parentNode;

    // parent.appendChild(parent, optionList);
    // parent.insertBefore(option, optionList);

    console.log("AFTER UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);
    console.log("Latest QuestionID : " + latestQuestionID);
}

function addQuestion() {

    console.log("\nBEFORE UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);
    console.log("Latest QuestionID : " + latestQuestionID);

    // important check keeping LOC
    count++;
    totalQuestionCount++;
    latestQuestionID++;
    radioCount = 1;
    totalRadioCount++;
    updateCountOnForm(count);




    const questionDiv = document.createElement('div');
    questionDiv.setAttribute('id', `sq${totalQuestionCount}`);
    questionDiv.setAttribute('class', `single_question${totalQuestionCount}`);


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
    radioOption1.setAttribute('type', 'checkbox');
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
    radioOption2.setAttribute('type', 'checkbox');
    radioOption2.setAttribute('placeholder', 'Options');
    radioOption2.setAttribute('name', `acoption${totalQuestionCount}${radioCount}`);

    individualOption2.appendChild(option2);
    individualOption2.appendChild(radioOption2);

    optionList.append(individualOption1);
    optionList.append(individualOption2);

    questionDiv.appendChild(individualQuestion);
    questionDiv.appendChild(optionList);
    
    // const hr = document.createElement('hr');

    // questionDiv.append(hr);

    const addButton = document.getElementById('addOptions');
    // //console.log(addButton);
    var parent = addButton.parentNode;

    // parent.appendChild(parent, option);
    parent.insertBefore(questionDiv, addButton);
    updateRadioCountOnForm(totalRadioCount);
    




    questionRadioCountArray.push([totalQuestionCount, radioCount]);

    rdc(questionRadioCountArray);
    
    console.log("AFTER UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);
    console.log("Latest QuestionID : " + latestQuestionID);
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
}

function updateAll() {
    updateCountOnForm(count);
    updateRadioCountOnForm(totalRadioCount);
    rdc(questionRadioCountArray);
}

function deleteQuestion(questionID) {
    console.log("\nBEFORE UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);
    console.log("Latest QuestionID : " + latestQuestionID);
    
    
    var classNameOfQuestionToRemove = "sq" + questionID;
    const element = document.getElementById(classNameOfQuestionToRemove);
    
    element.remove();
    count--;
    updateCountOnForm(count);
    totalRadioCount = totalRadioCount - radioCount;
    updateRadioCountOnForm(totalRadioCount);
    
    questionID = parseInt(questionID);
    if (questionID == totalQuestionCount) {
        totalQuestionCount--;
    }
    
    
    var double = questionRadioCountArray.pop();
    radioCount = double.pop();
    double.push(radioCount);
    questionRadioCountArray.push(double);
    
    
    
    var firstArray = [];
    for (var i = 0; i < questionRadioCountArray.length; i++) {
        firstArray.push(questionRadioCountArray[i][0]);
    }    
    var index = firstArray.indexOf(questionID);
    questionRadioCountArray.splice(index, 1);
    
    console.log(questionRadioCountArray[questionRadioCountArray.length-1]);
    latestQuestionID = parseInt(questionRadioCountArray[questionRadioCountArray.length-1][0]);
    
    rdc(questionRadioCountArray);

    console.log("AFTER UPDATE");
    console.log("Count: " + count, "totalQuestionCount: " + totalQuestionCount);
    console.log("questionRadioCount: " + questionRadioCountArray, "radioCount: " + radioCount);
    console.log("Latest QuestionID : " + latestQuestionID);
}

function do_resize(textbox) {

    var maxrows=5; 
    var txt=textbox.value;
    var cols=textbox.cols;
   
    var arraytxt=txt.split('\n');
    var rows=arraytxt.length; 
   
    for (i=0;i<arraytxt.length;i++) 
        rows+=parseInt(arraytxt[i].length/cols);
   
    if (rows>maxrows) textbox.rows=maxrows;
    else textbox.rows=rows;
}