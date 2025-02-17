$(function () {
    echart_overlap();
    echart_heat();
    echart_dui();
    echart_zhe();

    //table 4  第一个关系堆叠图
    function echart_overlap(){
         var myChart = echarts.init(document.getElementById('chart_overlap'));
        myChart.clear();
option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
   legend: {
              top:'8%',
              textStyle:{
                    color: '#fff'
                },

          },
  grid: {
    left: '5%',
    right: '5%',
    bottom: '5%',
    containLabel: true
  },
  xAxis: [
    { name: 'elec type name',
              nameGap: 25,  // x轴name与横坐标轴线的间距
    nameLocation: "middle", // x轴name处于x轴的什么位置
      type: 'category',
      data:[0,1,2,3,4,5,6,7,8,9,10],
          axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                }
    }
  ],
  yAxis: [
    {name: 'volt name percentage',
    nameRotate: 90, // y轴name旋转90度 使其垂直
    nameGap: 25,  // y轴name与横纵坐标轴线的间距
    nameLocation: "middle", // y轴name处于y轴的什么位置
      type: 'value',
          axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                }
    }
  ],
  series: [

    {
      name: '220V',
      type: 'bar',
      stack: 'Ad',

      emphasis: {
        focus: 'series'
      },
       data: [0.7498244245025361, 0.0, 0.5912698412698413, 0.4213197969543147, 0.0, 0.19148936170212766, 0.7232992597814593, 0.10526315789473684, 0.0, 0.5, 1.0]

    },
    {
      name: '380V',
      type: 'bar',
      stack: 'Ad',
      emphasis: {
        focus: 'series'
      },

    data: [0.011080764728833398, 0.375, 0.1111111111111111, 0.017766497461928935, 0.96875, 0.6170212765957447, 0.0034073551874045354, 0.3157894736842105, 1.0, 0.0, 0.0]

    },
    {
      name: '10000V',
      type: 'bar',
      stack: 'Ad',
      emphasis: {
        focus: 'series'
      },

     data: [0.2390948107686305, 0.625, 0.2976190476190476, 0.5609137055837563, 0.03125, 0.19148936170212766, 0.27329338503113615, 0.5789473684210527, 0.0, 0.5, 0.0]

    }
  ]
};

        option && myChart.setOption(option);
    }//table 4  第一个关系堆叠图
    function echart_heat(){
         var myChart = echarts.init(document.getElementById('chart_heat'));
        myChart.clear();

        // prettier-ignore
        const data = [[0, 0, -0.04], [0, 1, 0.45],  [0, 2, 0.37], [0, 3, 1.00],
        [1, 0, 0.03], [1, 1, 0.94], [1, 2, 1.00], [1, 3, 0.37],
        [2, 0, 0.03], [2, 1, 1.00], [2, 2, 0.94], [2, 3, 0.45],
         [3, 0, 1.00], [3, 1, 0.03], [3, 2, 0.03], [3, 3, -0.04]]
            .map(function (item) {
            return [item[1], item[0], item[2] || '-'];
        });
        option = {
          tooltip: {
            position: 'top'
          },
          grid: {

            top: '12%',
            left: '20%',bottom:'10%'
          },
          xAxis: {
            type: 'category',
            data: ['elec_type_name', 'volt_name', 'prc_name', 'contract_cap'],
            splitArea: {
              show: true
            },
          axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                }
          },
          yAxis: {
            type: 'category',
            data: ['contract_cap', 'prc_name', 'volt_name', 'elec_type_name'],
            splitArea: {
              show: true
            },
                axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                }
          },
          visualMap: {
            min: 0,
            max: 1,
            calculable: true,
               orient: 'vertical',
    left: 'right',
    bottom: 'center',
              inRange: {
            color: ['rgba(242,252,151,0.5)','rgba(3,193,197,0.5)']
        }
          },
          series: [
            {
              name: '相关度',
              type: 'heatmap',
              data: data,
              label: {
                show: true
              },

              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowColor: 'rgba(0,0,0,0.07)'
                }
              }
            }
          ]
        };

        option && myChart.setOption(option);
    }


    function echart_dui(){
         var myChart = echarts.init(document.getElementById('chart_dui'));
         myChart.clear();
         option = {
              tooltip: {
                trigger: 'axis',
                axisPointer: {
                  type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
                }
          },

          legend: {
              top:'18%',
              textStyle:{
                    color: '#fff'
                },
          },
          grid: {
            left: '10%',
              top:'30%',
            right: '8%',
            // bottom: '10%',
            containLabel: true
          },
          xAxis: {
              name: 'volt name percentage',
              nameGap: 25,  // x轴name与横坐标轴线的间距
              nameLocation: "middle", // x轴name处于x轴的什么位置
                splitLine:{
                    lineStyle:{
                        color:['#f2f2f2'],
                        width:0,
                        type:'solid'
                    },
                },
            type: 'value',
               axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                }
          },
          yAxis: {
              name: 'prc   name',
            nameRotate: 90, // y轴name旋转90度 使其垂直
            nameGap: 25,  // y轴name与横纵坐标轴线的间距
            nameLocation: "middle", // y轴name处于y轴的什么位置
            type: 'category',
            data: [0,1,2],
               axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                },
                splitLine:{
                    lineStyle:{
                        width:0,
                        type:'solid'
                    }
                }
          },
          series: [
            {
              name: '220 V',
              type: 'bar',
              stack: 'total',
              label: {
                show: false
              },
              emphasis: {
                focus: 'series'
              },
                        itemStyle:{
									normal:{color:'#8512c1'}
								},
              data:[0.7378018051037706, 0.0, 0.0]
            },
              {
              name: '380 V',
              type: 'bar',
              stack: 'total',
              label: {
                show: false
              },
              emphasis: {
                focus: 'series'
              },itemStyle:{
									normal:{color:'#0cbaba'}
								},
              data:[0.2621981948962294, 0.006329113924050633, 0.01293103448275862]  },
               {
              name: '10000 V',
              type: 'bar',
              stack: 'total',
              label: {
                show: false
              },
              emphasis: {
                focus: 'series'
              },        itemStyle:{
									normal:{color:'#bfbc10'}
								},
              data: [0.0, 0.9936708860759493, 0.9870689655172413]     }

          ]
        };

        option && myChart.setOption(option);
    }//table 4  第一个关系堆叠图
    function echart_zhe() {
    var myChart = echarts.init(document.getElementById('chart_zhe'));
            myChart.clear();
	option={
			title: {
				text: ''
			},
			tooltip: {
				orient: 'vertical',
                right: '1%',
                top: '20%',
                iconStyle: {
                    // color: '#fff',
                    borderColor: '#fff'
                    // borderWidth: 1,
                }
			},
          toolbox: {
                orient: 'vertical',
                right: '8%',
                top: '40%',
                iconStyle: {
                    color: '#fff',
                    borderColor: '#fff',
                    borderWidth: 1,
                },
                feature: {
                    saveAsImage: {},
                    magicType: {
                        // show: true,
                        type: ['line','bar','stack','tiled']
                    }
                }
            },
			legend: {
				top:60,
				right:5,
				textStyle:{
					color:'white'
				},
				orient:'vertical',
				data:[
						{name:'220 V',icon:'circle'},
						{name:'380 V',icon:'circle'},
						{name:'10000 V',icon:'circle'}
					],
			},
			grid: {
				left: '10%',
				right: '16%',
				bottom: '8%',
				top:'20%',
				containLabel: true
			},
			xAxis: {
			     name:'sample number',
                nameGap:25,
                nameLocation:'middle',
				type: 'category',
				boundaryGap: false,
				axisTick:{show:false},
				axisLabel:{
					textStyle:{
						color:"white", //刻度颜色
						fontSize:10  //刻度大小
						}
				},
				axisLine:{
					show:true,
					lineStyle:{
						color: 'white',
						width: 1,
						type: 'solid'
					}
				},
				data:  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
			},

			yAxis: {
			    name:'contract_cap',
                 nameRotate: 90, // y轴name旋转90度 使其垂直
                nameGap: 40,  // y轴name与横纵坐标轴线的间距
                nameLocation: "middle", // y轴name处于y轴的什么位置
				type: 'value',
				axisTick:{show:false},
				axisLabel:{
					textStyle:{
						color:"white", //刻度颜色
						fontSize:10  //刻度大小
						}
				},
				axisLine:{
					show:true,
					lineStyle:{
						color: 'white',
						width: 1,
						type: 'solid'
					}
				},
				splitLine:{
					show:false
				}
			},
			series: [
						{
							name:'220 V',
							type:'line',
							itemStyle : {
									normal : {
									color:'#F3891B'
								},
								lineStyle:{
									normal:{
									color:'#F3891B',
									opacity:1
										}
								}
							},
							data: [24.0, 38.0, 48.0, 10.0, 20.0, 10.0, 10.0, 10.0, 24.0, 10.0, 33.0, 3.0, 48.0, 12.0, 12.0, 100.0, 20.0, 20.0, 20.0, 10.0]
						},
						{
							name:'380 V',
							type:'line',
							itemStyle : {
									normal : {
									color:'#006AD4'
								},
								lineStyle:{
									normal:{
									color:'#F3891B',
									opacity:1
										}
								}
							},
							data: [200.0, 250.0, 80.0, 50.0, 180.0, 315.0, 500.0, 1000.0, 565.0, 200.0, 250.0, 250.0, 250.0, 500.0, 0.0, 250.0, 500.0, 250.0, 250.0, 1115.0]
						},
						{
							name:'10000 V',
							type:'line',
							itemStyle : {
									normal : {
									color:'#009895'
								},
								lineStyle:{
									normal:{
									color:'#009895',
									opacity:1
										}
								}
							},
							data: [2.0, 2.0, 2.0, 2.0, 2.0, 4.0, 2.0, 2.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 4.0, 4.0, 4.0, 2.0, 4.0]
						}
					]
		};


 option && myChart.setOption(option);
    }



});
