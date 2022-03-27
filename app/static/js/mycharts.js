function reset(divid){
  $(".panel").outerWidth($(".tab-pane").width());
  $(".panel-body").outerWidth($(".panel").width());
  $(".chart-div").outerWidth($(".panel-body").width());
  $(divid).removeAttr("_echarts_instance_").empty();
}


//时间线可视化
function  timeLine(source_data) {
    reset('#timeline');
    var myChart = echarts.init(document.getElementById('timeline'));
    var option;

    option = {
  title: {
    text: 'Basic Graph'
  },
  tooltip: {},
  animationDurationUpdate: 1500,
  animationEasingUpdate: 'quinticInOut',
  series: [
    {
      type: 'graph',
      layout: 'none',
      symbolSize: 50,
      roam: true,
      label: {
        show: true
      },
      edgeSymbol: ['circle', 'arrow'],
      edgeSymbolSize: [4, 10],
      edgeLabel: {
        fontSize: 20
      },
      data: [
        {
          name: 'Node 1',
          x: 300,
          y: 300
        },
        {
          name: 'Node 2',
          x: 800,
          y: 300
        },
        {
          name: 'Node 3',
          x: 550,
          y: 100
        },
        {
          name: 'Node 4',
          x: 550,
          y: 500
        }
      ],
      // links: [],
      links: [
        {
          source: 0,
          target: 1,
          symbolSize: [5, 20],
          label: {
            show: true
          },
          lineStyle: {
            width: 5,
            curveness: 0.2
          }
        },
        {
          source: 'Node 2',
          target: 'Node 1',
          label: {
            show: true
          },
          lineStyle: {
            curveness: 0.2
          }
        },
        {
          source: 'Node 1',
          target: 'Node 3'
        },
        {
          source: 'Node 2',
          target: 'Node 3'
        },
        {
          source: 'Node 2',
          target: 'Node 4'
        },
        {
          source: 'Node 1',
          target: 'Node 4'
        }
      ],
      lineStyle: {
        opacity: 0.9,
        width: 2,
        curveness: 0
      }
    }
  ]
};

    option && myChart.setOption(option);

}


//涉华专题1----时间X领域
function chinaField(){
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'china-field'},
    dataType: "json",
    success: function(data){
      chinaField2(data);
    },
    error: function(e){
      alert("error");
    }
  });
}
function chinaField2(data) {
  reset('#field-month');
  var chartDom = document.getElementById('field-month');
  var myChart = echarts.init(chartDom);
  var option;

  option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {},
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        data: ['2020第1季度','2020第2季度','2020第3季度','2020第4季度','2021第1季度','2021第2季度','2021第3季度','2021第4季度']
      }
    ],
    yAxis: [
      {
        type: 'value'
      }
    ],
    series: [
      //   {
      //   data: [820, 932, 901, 934, 1290, 1330, 1320],
      //   type: 'line',
      //   smooth: true
      // },
      // {
      //   name: 'Direct',
      //   type: 'bar',
      //   emphasis: {
      //     focus: 'series'
      //   },
      //   data: [320, 332, 301, 334, 390, 330, 320]
      // },

      // {
      //   name: '总数',
      //   type: 'bar',
      //   data: data[2],
      //   emphasis: {
      //     focus: 'series'
      //   }
      //   // markLine: {
      //   //   lineStyle: {
      //   //     type: 'dashed'
      //   //   },
      //   //   data: [[{ type: 'min' }, { type: 'max' }]]
      //   // }
      // },
      {
        name: '现代交通科技',
        type: 'bar',
        barWidth: 20,
        stack: '总数',
        emphasis: {
          focus: 'series'
        },
        data: data[1][0]
      },
      {
        name: '新代信息通信科技',
        type: 'bar',
        stack: '总数',
        emphasis: {
          focus: 'series'
        },
        data: data[1][1]
      },
      {
        name: '空天科技',
        type: 'bar',
        stack: '总数',
        emphasis: {
          focus: 'series'
        },
        data: data[1][2]
      },
      {
        name: '国防安全',
        type: 'bar',
        stack: '总数',
        emphasis: {
          focus: 'series'
        },
        data: data[1][3]
      },
      {
        name: '医药健康科技',
        type: 'bar',
        barWidth: 5,
        stack: '总数',
        emphasis: {
          focus: 'series'
        },
        data: data[1][4]
      },
      {
        name: '食品农业科技',
        type: 'bar',
        stack: '总数',
        emphasis: {
          focus: 'series'
        },
        data: data[1][5]
      },
      {
        name: '能源环境科技',
        type: 'bar',
        stack: '总数',
        emphasis: {
          focus: 'series'
        },
        data: data[1][6]
      },
      {
        name: '大数据与人工智能',
        type: 'bar',
        stack: '总数',
        emphasis: {
          focus: 'series'
        },
        data: data[1][7]
      },
      {
        name: '智能制造',
        type: 'bar',
        stack: '总数',
        emphasis: {
          focus: 'series'
        },
        data: data[1][6]
      },
      {
        name: '新材料科技',
        type: 'bar',
        stack: '总数',
        emphasis: {
          focus: 'series'
        },
        data: data[1][7]
      }
    ]
  };

option && myChart.setOption(option);

}

//涉华专题2----时间*数量--month为单位
function chinaNum(){
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'china-num'},
    dataType: "json",
    success: function(data){
      chinaNum2(data);
    },
    error: function(e){
      alert("error");
    }
  });
}
function chinaNum2(data) {
  reset('#china-num');
  var chartDom = document.getElementById('china-num');
  var myChart = echarts.init(chartDom);
  var option;
  let num = data[0];
  let time = data[1]
  option = {
    tooltip: {
    trigger: 'axis'
  },
  legend: {},
  toolbox: {
    show: true,
    feature: {
      dataZoom: {
        yAxisIndex: 'none'
      },
      dataView: { readOnly: false },
      magicType: { type: ['line', 'bar'] },
      restore: {},
      saveAsImage: {}
    }
  },
    xAxis: {
      type: 'category',
      name:'时间',
      data: time
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name:"政策数量",
        data: num,
        type: 'line',
        smooth: true
      }
    ]
  };

option && myChart.setOption(option);

}

//涉华专题3----时间*机构数量
function institutionNum(){
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'institution-num'},
    dataType: "json",
    success: function(data){
      institutionNum2(data);
    },
    error: function(e){
      alert("error");
    }
  });
}
function institutionNum2(data) {
  reset('#institution-num');
  var chartDom = document.getElementById('institution-num');
  var myChart = echarts.init(chartDom);
  var option;

  option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        // Use axis to trigger tooltip
        type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
      }
    },
    legend: {},
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: ['5月', '6月', '7月', '8月', '9月', '10月', '11月','12月']
    },
    series: [
      {
        name: data[0][0],
        type: 'bar',
        stack: 'total',
        label: {
          show: true
        },
        emphasis: {
          focus: 'series'
        },
        data: data[1][0]
      },
      {
        name: data[0][1],
        type: 'bar',
        stack: 'total',
        label: {
          show: true
        },
        emphasis: {
          focus: 'series'
        },
        data: data[1][1]
      },
      {
        name: data[0][2],
        type: 'bar',
        stack: 'total',
        label: {
          show: true
        },
        emphasis: {
          focus: 'series'
        },
        data: data[1][2]
      }
    ]
  };

  option && myChart.setOption(option);
  myChart.on('click',  function(param) {
  console.log("csac")
            //param.name x轴值,param.data y轴值
            alert(param.name+":"+param.data)
        });
}


//关键词饼图
function keywordsPie() {
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'china-keyword-pie'},
    dataType: "json",
    success: function(data){
      keywordsPie2(data);
    },
    error: function(e){
      alert("error");
    }
  });
}

function keywordsPie2(data) {
  reset('#keywords-tree');
  var chartDom = document.getElementById('keywords-tree');
var myChart = echarts.init(chartDom);
var option;

option = {
  title: {
    text: '涉华政策关键词演变图',
    subtext: '',
    left: 'center'
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b} : {c} ({d}%)'
  },
  legend: {
    left: 'center',
    top: 'bottom',
    data: [
      'rose1',
      'rose2',
      'rose3',
      'rose4',
      'rose5',
      'rose6',
      'rose7',
      'rose8'
    ]
  },
  toolbox: {
    show: true,
    feature: {
      mark: { show: true },
      dataView: { show: true, readOnly: false },
      restore: { show: true },
      saveAsImage: { show: true }
    }
  },
  series: [
    {
      name: '涉华关键词2020',
      type: 'pie',
      radius: [20, 140],
      center: ['25%', '50%'],
      roseType: 'radius',
      itemStyle: {
        borderRadius: 5
      },
      label: {
        show: true
      },
      emphasis: {
        label: {
          show: true
        }
      },
      data: data[0]
    },
    {
      name: '涉华关键词2021',
      type: 'pie',
      radius: [20, 140],
      center: ['75%', '50%'],
      roseType: 'area',
      itemStyle: {
        borderRadius: 5
      },
      data: data[1]
    }
  ]
};

option && myChart.setOption(option);

}
//涉华专题4----时间*关键词
function keywordsTree(){
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'china-keyword-tree'},
    dataType: "json",
    success: function(data){
      keywordsTree2(data);
    },
    error: function(e){
      alert("error");
    }
  });
}
function keywordsTree2(data) {
  reset('#keywords-tree');

var chartDom = document.getElementById('keywords-tree');
var myChart = echarts.init(chartDom);
var option;
  // myChart.hideLoading();
  myChart.setOption(
    (option = {
      tooltip: {
        trigger: 'item',
        triggerOn: 'mousemove'
      },
      series: [
        {
          type: 'tree',
          data: [data],
          top: '1%',
          left: '7%',
          bottom: '1%',
          right: '20%',
          symbolSize: 7,
          label: {
            position: 'left',
            verticalAlign: 'middle',
            align: 'right',
            fontSize: 16
          },
          leaves: {
            label: {
              position: 'right',
              verticalAlign: 'middle',
              align: 'left'
            }
          },
          emphasis: {
            focus: 'descendant'
          },
          expandAndCollapse: true,
          animationDuration: 550,
          animationDurationUpdate: 750
        }
      ]
    })
  );

option && myChart.setOption(option);

}

//国情咨文---时间*关键词
function stateMessageTree(){
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'state-message-tree'},
    dataType: "json",
    success: function(data){
      stateMessageTree2(data);
    },
    error: function(e){
      alert("error");
    }
  });
}

function stateMessageTree2(data) {
  reset('#state-message');
var chartDom = document.getElementById('state-message');
var myChart = echarts.init(chartDom);
var option;
  // myChart.hideLoading();
  myChart.setOption(
    (option = {
      tooltip: {
        trigger: 'item',
        triggerOn: 'mousemove'
      },
      series: [
        {
          type: 'tree',
          data: [data],
          top: '1%',
          left: '7%',
          bottom: '1%',
          right: '20%',
          symbolSize: 7,
          label: {
            position: 'left',
            verticalAlign: 'middle',
            align: 'right',
            fontSize: 16
          },
          leaves: {
            label: {
              position: 'right',
              verticalAlign: 'middle',
              align: 'left'
            }
          },
          emphasis: {
            focus: 'descendant'
          },
          expandAndCollapse: true,
          animationDuration: 550,
          animationDurationUpdate: 750
        }
      ]
    })
  );

option && myChart.setOption(option);
}
// 国家×年份
function countryYear(){
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'country-year'},
    dataType: "json",
    success: function(data){
      chartLine(data);
    },
    error: function(e){
      alert("error");
    }
  });
}

function chartLine(source_data){
  reset('#country-year');
  var countries = [];
  for (let line of source_data) {
    if (!(countries.find(item => (item == line[1]))) && line[0] < 2021 && line[0] > 2011) {
      countries.push(line[1]);
    }
  }
  var years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020];
  var series = [];
  for (let country of countries) {
    let line = {
      name: country,
      type: 'line',
      data: []
    }
    for (let year of years) {
      amount = source_data.find(item => (item[0] == year && item[1] == country));
      if (amount) {
        line.data.push(amount[2]);
      }
      else {
        line.data.push(0);
      }
    }
    series.push(line);
  }
  var myChart = echarts.init(document.getElementById('country-year'));
  var option = {
    tooltip: {
      trigger: 'axis'
    },

    legend: {
        data: countries
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: years
    },
    yAxis: {
        type: 'value'
    },
    series: series
  };
  myChart.setOption(option, true);
  window.onresize = myChart.resize;
}


// 领域×年份
function fieldYear(){
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'field-year'},
    dataType: "json",
    success: function(data){
      chartRiver(data);
    },
    error: function(e){
      alert("error");
    }
  });
}

function chartRiver(source_data){  
  reset('#field-year');
  for (let item of source_data) {
    item[0] = String(item[0])
  }
  var myChart = echarts.init(document.getElementById('field-year'));
  var themes = [];
  for (let item of source_data) {
    if (!themes.includes(item[2])) {
      themes.push(item[2]);
    }
  }
  var option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'line',
            lineStyle: {
                color: 'rgba(0,0,0,0.2)',
                width: 1,
                type: 'solid'
            }
        }
    },

    legend: {
        data: themes
    },

    toolbox: {
      feature: {
          saveAsImage: {}
      }
    },

    singleAxis: {
        top: 50,
        bottom: 50,
        axisTick: {},
        axisLabel: {},
        type: 'time',
        axisPointer: {
            animation: true,
            label: {
                show: true
            }
        },
        splitLine: {
            show: true,
            lineStyle: {
                type: 'dashed',
                opacity: 0.2
            }
        }
    },

    series: [
        {
            type: 'themeRiver',
            emphasis: {
                itemStyle: {
                    shadowBlur: 20,
                    shadowColor: 'rgba(0, 0, 0, 0.8)'
                }
            },
            data: source_data
        }
    ]
};
  myChart.setOption(option, true);
  window.onresize = myChart.resize;
}


// 国家×领域
function countryField(){
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'country-field'},
    dataType: "json",
    success: function(data){
      chartRadar(data);
    },
    error: function(e){
      alert("error");
    }
  });
}

function chartRadar(source_data){
  reset('#country-field');
  var countries = [];
  for (let line of source_data) {
    if (!(countries.find(item => (item == line[0])))) {
      countries.push(line[0]);
    }
  }
  var themes = [];
  for (let item of source_data) {
    if (!themes.includes(item[1])) {
      themes.push(item[1]);
    }
  }
  var maxamount = 0;
  for (let item of source_data) {
    if (item[2] > maxamount) {
      maxamount = item[2];
    }
  }
  var indicator = [];
  for (let theme of themes) {
    indicator.push({name: theme, max: maxamount});
  }
  var series = [];
  for (country of countries) {
    let line = {name: country, value: []};
    for (let theme of themes) {
      amount = source_data.find(item => (item[0] == country && item[1] == theme));
      if (amount) {
        line.value.push(amount[2]);
      }
    }
    series.push(line);
  }
  var myChart = echarts.init(document.getElementById('country-field'));
  var option = {
    tooltip: {},
    legend: {
        data: countries
    },
    radar: {
        // shape: 'circle',
        name: {
            textStyle: {
                color: '#fff',
                backgroundColor: '#999',
                borderRadius: 3,
                padding: [3, 5]
            }
        },
        indicator: indicator
    },
    series: [{
        type: 'radar',
        // areaStyle: {normal: {}},
        data: series
    }]
};
  myChart.setOption(option, true);

  window.onresize = myChart.resize;
}

// 颠覆性技术词云图
function wordCloud(){
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'word-cloud'},
    dataType: "json",
    success: function (data){
      drawCloud(data);
    },
    error: function (e){
      alert("error");
    }
  });
}

function drawCloud(source_data) {
  var shownum = $("#shownum").val();
  var techlist = [];
  for (let item of source_data){
    techlist = techlist.concat(item);
  }
  var techcount = {};
  for (let tech of techlist){
    if (tech){
      if (tech in techcount){
        techcount[tech] += 1;
      } else {
        techcount[tech] = 1;
      }
    }
  }
  var series = [];
  for (let tech in techcount) {
    series.push([tech, techcount[tech]]);
  }
  series = series.sort(function(a,b){return b[1]-a[1]});
  if (series.length > shownum) {
    series = series.slice(0, shownum);
  }
  var option = {
    tooltip: {
        show: true,
        formatter: function(item) {
            return item[0] + ' 出现 ' + item[1] + ' 次'
        }
    },
    list: series,
    color: 'random-dark',
    shape: 'circle',
    ellipticity: 1,
    noDataLoadingOption: {          // 无数据提示
      backgroundColor: '#eee',
      text: '暂无数据',
      textStyle: {
        color: '#888',
        fontSize: 14
      }
    }
  }
  var wc = new Js2WordCloud(document.getElementById('word-cloud'));
  wc.showLoading({
      backgroundColor: '#fff',
      text: '正在加载词云图',
      effect: 'spin'
  });

  setTimeout(function() {
      wc.setOption(option);
  }, 1000);

  window.onresize = function() {
    wc.resize();
}
}


//涉华关键词词云图
function chinaCloud() {
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'china-cloud'},
    dataType: "json",
    success: function(data){
      chinaCloud2(data);
    },
    error: function(e){
      alert("error");
    }
  });
}

function chinaCloud2(source_data) {
  reset('#keywords-tree');

  var myChart = echarts.init(document.getElementById('keywords-tree'));
  // var shownum = $("#keyshownum").val();
  var keylist = [];
  for (let item of source_data) {
    keylist = keylist.concat(item[0].split(', '));
  }
  var keycount = {};
  for (let key of keylist) {
    if (key) {
      if (key in keycount) {
        keycount[key] += 1;
      } else {
        keycount[key] = 1;
      }
    }
  }
  var series = [];
  for (let key in keycount) {
    series.push([key, keycount[key]]);
  }
  series = series.sort(function (a, b) {
    return b[1] - a[1]
  });
  if (series.length > shownum) {
    series = series.slice(0, shownum);
  }
  var option = {
    tooltip: {
      show: true,
      formatter: function (item) {
        return item[0] + ' 出现 ' + item[1] + ' 次'
      }
    },
    list: series,
    color: 'random-dark',
    shape: 'circle',
    ellipticity: 1,
    noDataLoadingOption: {          // 无数据提示
      backgroundColor: '#eee',
      text: '暂无数据',
      textStyle: {
        color: '#888',
        fontSize: 14
      }
    }
  }
  var keywc = new Js2WordCloud(document.getElementById('keywords-tree'))
  keywc.showLoading({
    backgroundColor: '#fff',
    text: '正在加载词云图',
    effect: 'spin'
  })

  setTimeout(function () {
    keywc.setOption(option);
  }, 1000);

  window.onresize = function () {
    keywc.resize();
  }

}

// 关键词词云图
function keywordCloud(){
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'china-keyword-cloud'},
    dataType: "json",
    success: function (data){
      drawkeyCloud(data);
    },
    error: function (e){
      alert("error");
    }
  });
}

function drawkeyCloud(source_data) {
  var current_word = ""
  var shownum = $("#keyshownum").val();
  var keylist = [];
  for (let item of source_data) {
    keylist = keylist.concat(item[0].split(', '));
  }
  var keycount = {};
  for (let key of keylist) {
    if (key) {
      if (key in keycount) {
        keycount[key] += 1;
      } else {
        keycount[key] = 1;
      }
    }
  }
  var series = [];
  for (let key in keycount) {
    series.push([key, keycount[key]]);
  }
  series = series.sort(function (a, b) {
    return b[1] - a[1]
  });
  if (series.length > shownum) {
    series = series.slice(0, shownum);
  }
  var option = {
    tooltip: {
      show: true,
      formatter: function (item) {
        window.current_word = item[0]
        return item[0] + ' 出现 ' + item[1] + ' 次'

      }
    },
    list: series,
    color: 'random-dark',
    shape: 'circle',
    ellipticity: 1,
    noDataLoadingOption: {          // 无数据提示
      backgroundColor: '#eee',
      text: '暂无数据',
      textStyle: {
        color: '#888',
        fontSize: 14
      }
    }
  }
  var keywc = new Js2WordCloud(document.getElementById('key-word-cloud'))
  keywc.showLoading({
    backgroundColor: '#fff',
    text: '正在加载词云图',
    effect: 'spin'
  })

  setTimeout(function () {
    keywc.setOption(option);
  }, 1000);

  // keywc.on('click',  function(param) {
  //       console.log("csac")
  //           //param.name x轴值,param.data y轴值
  //           alert(param.name+":"+param.data)
  //       });
  window.onresize = function () {
    keywc.resize();
  }
}

// 定制化分析
function customizedAna(){
  var keyword = $("#c_keyword").val();
  var domain = $("#c_domain").val();
  var type2 = $("#c_chart").val();
  console.log(domain+keyword+type2)
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'customizedAna','keyword':keyword,'domain':domain,'type':type2},
    dataType: "json",
    success: function (data){
      console.log("type:"+type2)
      customizedChart(data,type2);
    },
    error: function (e){
      alert("error");
    }
  });
}

function customizedChart(data,type){
  console.log(data)
  if(type=="number_institute"){
    reset('#customized');
    var chartDom = document.getElementById('customized');
    var myChart = echarts.init(chartDom);
    var option;
    option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [
      {
        name: 'Access From',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '40',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data
      }
    ]
  };
    option && myChart.setOption(option);
  }
  else{
    reset('#customized');
      var chartDom = document.getElementById('customized');
      var myChart = echarts.init(chartDom);
      var option;
      let num = data[0];
      let time = data[1]
      option = {
        tooltip: {
        trigger: 'axis'
      },
      legend: {},
      toolbox: {
        show: true,
        feature: {
          dataZoom: {
            yAxisIndex: 'none'
          },
          dataView: { readOnly: false },
          magicType: { type: ['line', 'bar'] },
          restore: {},
          saveAsImage: {}
        }
      },
        xAxis: {
          type: 'category',
          name:'时间',
          data: time
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name:"政策数量",
            data: num,
            type: 'line',
            smooth: true
          }
        ]
      };

    option && myChart.setOption(option);
  }
}

function searchKeywords(){
  console.log(window.current_word)
  word = window.current_word
  window.location.href = 'search.html?query=' + word + "&field=全部分类&order=rank&query-type=关键词";
  return false
};

$(document).ready(function () {
  institutionNum();
})
