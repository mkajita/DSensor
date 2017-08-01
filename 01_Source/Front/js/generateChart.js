/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

$.getJSON('http://172.24.215.178:9000/v2/humidity' , null, generateChart);

function generateChart(jsonData)
{
    // Jsonを解析
    recent_humidity = jsonData["recent_humidity"];
    humidity_level = jsonData["humidity_level"];
    day = jsonData["day"];

    // ラベルをセット
    var dateTimeArray = ['x'];
    var dateArray = [];
    var humidityArray = ['湿度の推移'];

    for(var i =0; i < day.length; i++)
    {
        var dateData = day[i];
        // yyyymmddの形式からyyyy-mm-ddの形式に変更
        var dateString = String(dateData['date']).substring(0,4) + '-' + String(dateData['date']).substring(4,6) + '-' + String(dateData['date']).substring(6,8);
        dateArray.push(dateString + ' 0:00:00');
        for(var j = 0; j < dateData['humidityinfo'].length; j++)
        {
            var humidityData = dateData['humidityinfo'];
            var dateHumidityData = humidityData[j];
            var humidity = dateHumidityData['humidity'];
            var dateTime = String(dateString) + ' ' + dateHumidityData['time'] + ':00:00';
            dateTimeArray.push(dateTime);
            humidityArray.push(humidity);
        }
    }
    
    // 画面左側表示部分の作成
    createHumidityInfo(recent_humidity, humidity_level);

    // グラフ作成
    var chart = c3.generate({
        bindto: '#chart',
        data: {
            x: 'x',
            xFormat: '%Y-%m-%d %H:%M:%S',
            columns: [
                //↓DBから取得したデータを動的に格納
                dateTimeArray,
                humidityArray
            ]
        },
        axis: {
            x: {
                label: {
                    text: '日時',
                    position: 'outer-middle'
                },
                type: 'timeseries',
                tick: {
                    format: '%m月%d日%H時',
                    //↓各日0時のみ動的に格納
                    values: dateArray
                }
            },
            y: {
                label: {
                    text: '湿度(%)',
                    position: 'outer-middle'
                },
                max: 100 //100%
            }
        }
    });
};
