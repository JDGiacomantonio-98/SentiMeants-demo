function sentiment_all_avg_chart_bars(scores,context) {
    var chart = new Chart(context, {
        type:'bar',
        data:{
            labels:[""],
            datasets:[{
                       label:'Negative Score',

                       data:[
                            scores[0]
                            ],
                       backgroundColor: background_color_gradient(-scores[0]),
                       borderWidth:2,
                       borderColor: "#990000",
                       },
                       {
                       label:"Positive Score",
                       data:[
                            scores[1]
                            ],
                       backgroundColor:background_color_gradient(scores[1]),
                       borderWidth:2,
                       borderColor: "#009900",
                       }]
            },
        options:{
            legend: {
                display: true,
                labels: {
                    fontFamily:"'Helvetica', 'Arial', 'sans-serif'",
                    fontColor:'#000',
                    fontSize:18,
                },
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMax: 1,
                        suggestedMin: 0,

                        defaultFontSize: 20,
                        },
                    }],
                    xAxes: [{
                        ticks:{

                        }
                    }],

            },
            responsive:true,
            maintainAspectRatio:false,
            devicePixelRatio:3,
        }
    });
    return chart;
}


function sentiment_tot_avg_chart_bars(score,context){
    var chart = new Chart(context, {
        type:'bar',
        data:{
            labels:[""],
            datasets:[{

                       label:"Total Score",
                       data:[
                            score
                            ],
                       backgroundColor:background_color_gradient(score),
                       borderColor:border_color_gradient(score),
                       borderWidth:2,


                    }]
        },
        options:{
            legend: {
                display: true,
                labels: {
                    fontFamily:"'Helvetica', 'Arial', 'sans-serif'",
                    fontColor:'#000',
                    fontSize:18,
                },
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMax: 1,
                        suggestedMin: -1,
                        },
                    }],
            },
            responsive:true,
            maintainAspectRatio:false,
            title: {
                display: false,
                text: 'Total Sentiment in Past 7 Days',
                fontSize: 36
            },
            devicePixelRatio:3, 
        }
    })
    return chart;
}


function timeseries_chart(scores,context){
    var unix_dates = Object.values(scores["date"]);
    var dates = Object.values(scores["date"]).map(unix_to_date);
    var chart = new Chart(context, {
        type: 'line',
        data:{
            labels:dates,
            datasets:chart_data_iterator(scores),
        },
        options:{
            legend: {
                display: true,
                labels: {
                    fontFamily:"'Helvetica', 'Arial', 'sans-serif'",
                    fontColor:'#000',
                    fontSize:18,
                },
            },
            tooltips:{
                enabled:false
            },
            scales: {
                yAxes:[{
                    stacked: false
                }],
                xAxes: [{
                    type: 'time',
                    time: {
                        unit: 'day',
                        distribution: 'linear',
                        },
                    ticks:{
                        source : "data"
                        }
                }],
            },
            responsive:true,
            maintainAspectRatio:false,
            devicePixelRatio:2,
        },
    });
    return chart
}


function polarity_chart(score,context){
    var chart = new Chart(context, {
        type:'bar',
        data:{
            labels:[""],
            datasets:[{

                       label:"Polarity",
                       data:[
                            score
                            ],
                       backgroundColor:polarity_color_gradient(score),
                       borderColor:border_color_gradient(score),
                       borderWidth:2,


                    }]
        },
        options:{
            legend: {
                display: true,
                labels: {
                    fontFamily:"'Helvetica', 'Arial', 'sans-serif'",
                    fontColor:'#000',
                    fontSize:18,
                },
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMax: 1,
                        suggestedMin: 0,
                        },
                    }],
            },
            responsive:true,
            maintainAspectRatio:false,
            title: {
                display: false,
                text: 'Total Sentiment in Past 7 Days',
                fontSize: 36
            },
            devicePixelRatio:3,
        }
    })
    return chart;
}

function unix_to_date(unix_date){
    var date = new Date(unix_date);
    return date
}


function chart_data_iterator(data){

    var keys = Object.keys(data);
    var table = [];
    var labels = ["Dates","Negative Sentiment","Positive Sentiment","Total Sentiment"];
    var colors = ["","#CC0000","#00CC00",""]
    for (i in keys){
        if ((keys[i] !== "date") && (keys[i] !== "comp_sent") && (keys[i] !== "polarity")){
            var datasets = {
                label:labels[i],
                data:Object.values(data[Object.keys(data)[i]]),
                backgroundColor:colors[i],
                borderColor:colors[i],
                fill:false,
                pointRadius:0
            }
            table.push(datasets)
        }


    }
    return table
}
function extract_daily_data(data){
    var keys = Object.keys(data);
    var src = [];
    for (i in keys){
        if (keys[i] != "date"){
                var array = Object.values(data[keys[i]]);
                src.push(array[array.length-1]);
            }
        }
    return src
}

function background_color_gradient(score){
    if (score < -0.75){
        return "#990000";
    }
     else if (score >= -0.75,score < -0.5){
        return "#CC0000";
    }
     else if (score >= -0.5,score < -0.25){
        return "#FF3333";
    }
     else if (score >= -0.25,score < -0.05){
        return "#FF6666";
    }
     else if (score >= -0.05,score < 0){
        return "#FF9999";
    }
     else if (score >= 0.05,score >= 0){
        return "#99FF99";
    }
     else if (score >= 0.05,score < 0.25){
        return "#66FF66";
    }
     else if (score >= 0.25,score < 0.5){
        return "#33FF33";
    }
     else if (score >= 0.5,score < 0.75){
        return "#00CC00";
    }
    else{
        return "#009900";
    }
}

function polarity_color_gradient(score){
    if (score>0, score<=0.11){
        return "#009900"
    }
    if (score>0.11, score<=0.22){
        return "#66ff33"
    }
    if (score>0.22, score<=0.33){
        return "#99ff33"
    }
    if (score>0.33, score<=0.44){
        return "#ccff33"
    }
    if (score>0.44, score<=0.55){
        return "#ffff00"
    }
    if (score>0.55, score<=0.66){
        return "#ffcc00"
    }
    if (score>0.66, score<=0.77){
        return "#ffaa00"
    }
    if (score>0.77, score<=0.88){
        return "#ff6600"
    }
    if (score>0.88, score<=0.99){
        return "#ff0000"
    }
    if (score>0.99){
        return "#990000"
    }

}
function border_color_gradient(score){
     if (score < -0.05){
        return "#990000";
     }
     else if (score <= -0.05,score <= 0.05){
        return "#404040";
     }
     else{
        return "#009900";
     }

}

