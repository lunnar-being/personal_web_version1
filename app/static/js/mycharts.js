function reset(divid){
  $(".panel").outerWidth($(".tab-pane").width());
  $(".panel-body").outerWidth($(".panel").width());
  $(".chart-div").outerWidth($(".panel-body").width());
  $(divid).removeAttr("_echarts_instance_").empty();
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




// 关键词词云图
function keywordCloud(){
  $.ajax({
    url: "/analysis_data",
    type: "POST",
    data: {'chart': 'key-word-cloud'},
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

  window.onresize = function () {
    keywc.resize();
  }
}


$(document).ready(function () {
  countryYear();
})


