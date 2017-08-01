/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
function createHumidityInfo(humidity, humidityLevel)
{
    // 画面左部の作成
    var addHtmlString = "<h2>湿度</h2>" + "<p>" + humidity + "%</p>" + "<h2>状態</h2>";
    if(humidityLevel === 0)
    {
       addHtmlString += "<p-dry>DRY</p-dry>";
    }
    else if(humidityLevel === 2)
    {
        addHtmlString += "<p-wet>WET</p-wet>";
    }
    else
    {
        addHtmlString += "<p>OK</p>";
    }
    document.getElementById('humidityInfo').innerHTML = addHtmlString;
}