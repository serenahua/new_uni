$(document).ready(function() {
  // 初始化記帳頁
  if ($('#tracking_management').length != 0) {
    let date = new Date();
    let year = date.getFullYear();
    let month = date.getMonth()+1;
    let first_day = getFirstDayInMonth(year, month);
    let days = getDaysInMonth(year, month);
    fillInCalendar(first_day, days);

    $('#chosen_month').MonthPicker({
      Button: false,
      MonthFormat: 'yy-mm',
      AltFormat: 'yy-mm-dd',
      Position: {
        of: $('#month_choose_label')
      },
      OnAfterChooseMonth: function(e) {
        $("#month_choose_label").text($("#chosen_month").val());
        let year = $(this).MonthPicker('GetSelectedYear');
        let month = $(this).MonthPicker('GetSelectedMonth');

        let first_day = getFirstDayInMonth(year, month);
        let days = getDaysInMonth(year, month);

        fillInCalendar(first_day, days);
      },
    });
  }

  // 初始化報表頁
  if ($('#report_management').length != 0 && $('#chosen_month').length != 0) {
    let year_month = $('#chosen_month').val().split('/');
    let year = parseInt(year_month[1]);
    let month = parseInt(year_month[0]);
    let first_day = getFirstDayInMonth(year, month);
    let days = getDaysInMonth(year, month);
    fillInCalendar(first_day, days);

    let data = JSON5.parse(received_data);
    fillInCalendarData(tab, data);

    $('#chosen_month').MonthPicker({
      Button: false,
      MonthFormat: 'yy-mm',
      AltFormat: 'yy-mm-dd',
      Position: {
        of: $('#month_choose_label')
      },
      OnAfterChooseMonth: function(e) {
        $("#month_choose_label").text($("#chosen_month").val());
        let url = $('#report_management').data('url');
        let year = $(this).MonthPicker('GetSelectedYear');
        let month = $(this).MonthPicker('GetSelectedMonth');

        window.location.href = `${url}?date=${year}-${month}-01&t=m&tab=${tab}`
      },
    });
  }

  function fillInCalendarData(tab, data) {
    for (let i of data) {
      let _d = parseInt(i.str_d.split('-')[2])
      let _d_item = $(`#date_${_d}`);
      let item = _d_item.closest('.active_item');

      if (i.hasOwnProperty('chicken')) {
        if (tab == 0 || tab == 1) {
          let $chicken = item.find('.tag.has_chicken span');
          let num = parseInt($chicken.text());
          let result = num+parseInt(i.chicken);
          if (result > 0) {
            $chicken.parent().removeClass('hide');
            $chicken.text(result);
          }
        }
      }
      if (i.hasOwnProperty('income')) {
        if (tab == 0 || tab == 1) {
          item.find('.dot.has_income').removeClass('hide');
        } else {
          let $income = item.find('.tag.has_income span');
          let num = parseInt($income.text());
          $income.parent().removeClass('hide');
          $income.text(num+parseInt(i.income));
        }
      }
      if (i.hasOwnProperty('expense')) {
        if (tab == 0 || tab == 1) {
          item.find('.dot.has_expense').removeClass('hide');
        } else {
          let $expense = item.find('.tag.has_expense span');
          let num = parseInt($expense.text());
          $expense.parent().removeClass('hide');
          $expense.text(num+parseInt(i.expense));
        }

      }
      if (i.has_remark) {
          item.find('.dot.has_remark').removeClass('hide');
      }
    }
  }

  //取得指定月份初始日
  function getFirstDayInMonth(year, month) {
    let m = ("0" + month).slice(-2);
    let day = new Date(year + "-" + m + "-01").getDay();
    return day;
  }

  //取得指定月份有幾天
  function getDaysInMonth(year, month) {
    return new Date(year, month, 0).getDate();
  }

  //填入月曆日期
  function fillInCalendar(first_day, days) {
      let day=0;
      for (let i=0;i<42;i++) {
          if (i<first_day) {
              $('#calendar_cell_'+i).removeClass('active_item');
              $('#calendar_cell_'+i).find('.item_text').text('');
              $('#calendar_cell_'+i).find('.item_text').removeAttr('id');
          } else if (i<(first_day+days)) {
              $('#calendar_cell_'+(first_day+day)).addClass('active_item');
              $('#calendar_cell_'+(first_day+day)).find('.item_text').text((day+1));
              $('#calendar_cell_'+(first_day+day)).find('.item_text').attr('id', `date_${day+1}`);
              day++;
          } else {
              $('#calendar_cell_'+i).removeClass('active_item');
              $('#calendar_cell_'+i).find('.item_text').text('');
              $('#calendar_cell_'+i).find('.item_text').removeAttr('id');
          }
      }
  }

  //點擊日期填寫記帳表單
  $('#tracking_management').on('click', '.active_item', function() {
      let year_month = $('#month_choose_label').text();
      let date = ("0" + ($(this).find('.item_text').text())).slice(-2);

      window.location.href = '/tracking/form?date='+year_month+'-'+date;
  })

  //點擊日期進入單日報表
  $('#report_management').on('click', '.active_item', function() {
      let year_month = $('#month_choose_label').text().split("-");
      let year = year_month[0];
      let month = year_month[1];
      let date = ("0" + ($(this).find('.item_text').text())).slice(-2);
      let url = $('#report_management').data('url');

      window.location.href = `${url}?t=d&date=${year}-${month}-${date}&tab=${tab}`;
  })

})