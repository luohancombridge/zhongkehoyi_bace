//通过率折线图，第一个参数div 句柄，第二个为x走坐标列表,第三个为折现值列表
function  zhexianpic(elem,x_data,y_data)
{

    var myChart = echarts.init(elem);
    option={
        title : {
            text: '通过率变化',
            subtext: '全部'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['通过率']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: x_data
        },
        yAxis:[
            {
                type: 'value',
                axisLabel:{
                    formatter:'{value} %'
                }
            }
        ],
        series: [{
            name: '通过率',
            type: 'line',
            stack: '总量',
            data: y_data
        }]
    }
    myChart.setOption(option)
}
//第一个为title列表【主title，副title】,第二个为div元素，第三个为x周值，第四个为y轴值
function  zhuzhuang_pic(title,ele,x_data,y_data)
{
    var y_data_yuan=[]
    // for (var i=0;i<y_data.length;i++)
    // {
    //     y_data_yuan.push(
    //         {
    //             name:'通过case',
    //             type:'bar',
    //             itemStyle: {normal: {color:'rgba(193,35,43,1)', label:{show:true}}},
    //             data:y_data[i]
    //         }
    //     )
    // }
    var tongguolv = echarts.init(ele);
    option = {
        title : {
            text: title[0],
            subtext: title[1]
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:[
                '通过case','失败case','出错case'
            ]
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        grid: {y: 70, y2:30, x2:20},
        xAxis : [
            {
                type : 'category',
                data : x_data
            },
            {
                type : 'category',
                axisLine: {show:false},
                axisTick: {show:false},
                axisLabel: {show:false},
                splitArea: {show:false},
                splitLine: {show:false},
                data : x_data
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [


            {
                name:'通过case',
                type:'bar',
                barWidth : 20,
                itemStyle: {normal: {color:'rgba(181,195,52,1)', label:{show:true}}},
                data:y_data[0]
            },
            {
                name:'失败case',
                type:'bar',
                barWidth : 20,
                itemStyle: {normal: {color:'rgba(193,35,43,1)', label:{show:true,textStyle:{color:'#27727B'}}}},
                data:y_data[1]
            },
            {
                name:'出错case',
                barWidth : 20,
                type:'bar',
                itemStyle: {normal: {color:'rgba(252,206,16,1)', label:{show:true,textStyle:{color:'#E87C25'}}}},
                data:y_data[2]
            }
        ]
    };
    tongguolv.setOption(option)
}


//圈图,第一个为元素句柄，第二个为分项目，第三个为数据列表
function   quantu(ele,xiangmu,deta_detail)
{
    var tongguolv = echarts.init(ele);
    var z=[]
    for (i=0;i<xiangmu.length;i++)
    {
        z.push({value:deta_detail[i], name:xiangmu[i]})
    }

    option = {
        title : {
            text: '测试统计',
            subtext: '最新一次',
            x:'center'
        },
        color:['green', 'red','yellow'],
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data:xiangmu
        },
        series: [
            {
                name:'访问来源',
                type:'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '30',
                            fontWeight: 'bold'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data:z
            }
        ]
    };
    tongguolv.setOption(option)
}