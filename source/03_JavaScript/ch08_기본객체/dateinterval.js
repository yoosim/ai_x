Date.prototype.getIntervalDay = function(otherday){
	// this와 otherday 사이의 날짜 수를 return
	// now.getInterbalDay(openday) : this=now , otherday = openday
	// openday.getInterbalDay(now) : this=openday, otherday = now
	// if(this > otherday){ //this(뒷날짜)가 큰게 맞다면
	// 	var intervalMilliSec = this.getTime() - otherday.getTime(); //let이 아닌 var로 선언해야 함
	// }else{
	// 	var intervalMilliSec = otherday.getTime() - this.getTime();
	// }
	// var intervalMilliSec = (this > otherday)?
	// 												(this.getTime() - otherday.getTime()):
	// 												(otherday.getTime() - this.getTime());
	var intervalMilliSec = Math.abs(this.getTime()- otherday.getTime());
	let day = intervalMilliSec / (1000*60*60*24);
	return Math.trunc(day); //Math.trunc(내림) Math.round(반올림) Math.cell(올림)
};
// let now = new Date();
// let openday = new Date(2025, 3, 4, 9, 30,0);
// console.log(now.getIntervalDay(openday),'일');
// console.log(openday.getIntervalDay(now), '일');