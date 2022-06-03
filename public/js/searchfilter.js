

const documentRef = useRef(document);


target = "target";
value = "value"

var ageArr = new Array(); //필터 내용을 저장하는 배열
var showFilterValue = document.getElementById("showFilter");//필터입력값 보여주기 위한 text

//필터 내용을 저장하는 function
function makeFilter(target){

    var ageVal = target.value; //check value
    var confirmCheck = target.checked; //check여부 확인
    console.log("필터 선택값 : "+ageVal);
    console.log("선택여부 : "+confirmCheck);

    // check true
    if(confirmCheck == true){

        console.log("check");
        ageArr.push(ageVal); // check value filter 배열에 입력

    // check false
    }else{

        ageArr.splice(ageArr.indexOf(ageVal), 1); // check value filter 배열내용 삭제            
    }

    showFilterValue.value = ageArr; // textBox에 필터 배열 추가
    console.log("필터입력값 출력 : "+ageArr);

}