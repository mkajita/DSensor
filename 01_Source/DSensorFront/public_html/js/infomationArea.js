/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var humidity = 60; // DBから取得した現在の湿度を入力
document.write("<h2>湿度</h2>");
document.write("<p>" + humidity + "%</p>");

document.write("<h2>状態</h2>");
if(humidity <= 30)
{
    document.write("<p-dry>DRY</p-dry>");
}
else if(humidity >= 70)
{
    document.write("<p-wet>WET</p-wet>");
}
else
{
    document.write("<p>OK</p>");
}