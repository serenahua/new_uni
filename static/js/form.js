$(document).ready(function() {
  // 訊息視窗彈出
  function openMsgWindow(type, title, content, callback = null) {
    const msgWindow = $('#msg_window');
    msgWindow.addClass(type);
    msgWindow.find('.title').html(title);
    msgWindow.find('.content').html(content);
    msgWindow.addClass('show');

    function closeMsgWindow() {
        msgWindow.removeClass(type);
        msgWindow.removeClass('show');
    }

    msgWindow.on('click', '.btn_ok, .btn_yes', function (e) {
        e.preventDefault();
        closeMsgWindow();
        if (callback !== null) callback();
    });

    msgWindow.on('click', '.btn_no', function (e) {
        e.preventDefault();
        closeMsgWindow();
    });
  }

  // 表單驗證
  function checkRequired(form) {
    var isValid = true;

    // 檢查所有带有 '.required' 的输入框
    form.find('.required').each(function () {
      var inputValue = $(this).val();

      if (!inputValue) {
          $(this).focus();
          isValid = false;
          return false;
      }
    });

    return isValid; // 返回驗證狀態
  }

  // ajax表單送出
  function postAjax(url, data, callback) {
    $.ajax({
      type: 'POST',
      url: url,
      data: data,
      success: function(rep) {
        callback(rep)
      }
    })
  }

  // 更新收入/支出標籤
  function updateTypeLabels(selectedLabel, otherLabel) {
    const selectedLabelTxt = selectedLabel == 'income' ? "收入" : "支出";
    const otherLabelTxt = otherLabel == 'income' ? "收入" : "支出";
    $(`label[for="${selectedLabel}"]`).html(`<i class='fa-solid fa-check'></i>${selectedLabelTxt}`);
    $(`label[for="${otherLabel}"]`).html(otherLabelTxt);
  }

  // 更新馥香雞/日料/家庭標籤
  function updateCategoryLabels(selectedLabel) {
    const types = ['chicken', 'hot_pot', 'house'];
    const types_text = ['馥香雞', '日料', '家庭'];

    for (var i=0;i<types.length;i++) {
      if (types[i] == selectedLabel) {
        $(`label[for="select_${types[i]}"]`).html(`<i class='fa-solid fa-check'></i>${types_text[i]}`);
      } else {
        $(`label[for="select_${types[i]}"]`).html(`${types_text[i]}`);
      }
    }

    showChickenIncomeItem(selectedLabel);
  }

  // 更新馥香雞收入選項
  function showChickenIncomeItem(selectedLabel) {
    let selectedType = $('input[name="type"]:checked').val();
    let $chicken_item = $('.chicken_income_item');

    if (selectedLabel == 'chicken' && selectedType == 'income') {
        toggleItemVisibility($chicken_item, true);
        toggleItemRequired($chicken_item, true);
    } else {
        toggleItemVisibility($chicken_item, false);
        toggleItemRequired($chicken_item, false);
    }
  }

  // 更新不同類別的支出項目選項
  function switchExpenseOptionsFromCategory(category) {
    const expenseItems = JSON5.parse(received_data);

    const categoryDropdown = $('#category');

    categoryDropdown.empty();
    categoryDropdown.append(`<option value="" disabled selected>請選擇項目</option>`)

    let data;
    switch (category) {
      case 'chicken':
        data = expenseItems.chicken;
        break;
      case 'hot_pot':
        data = expenseItems.hotpot;
        break;
      default:
        data = expenseItems.house;
    }

    for (let item of data) {
      categoryDropdown.append(`<option value="${item.id}">${item.name}</option>`);
    }
  }

  // 切換項目可見性
  function toggleItemVisibility(selector, isVisible) {
    if (isVisible) {
        $(selector).removeClass('hide');
    } else {
        $(selector).addClass('hide');
    }
  }

  // 切换項目是否必填
  function toggleItemRequired(selector, isRequired) {
    if (isRequired) {
        $(selector).find('.item_required').addClass('required');
    } else {
        $(selector).find('.item_required').removeClass('required');
    }
  }

  // 切換收入/支出類型
  $('#tracking_management, #chicken_management, #hotpot_management').on('click', 'input[name="type"]', function (e) {
    let selectedType = $(this).val();
    let selectedLabel = $('input[name="item_name"]:checked').val();

    // 根據所選類別切換項目可見性及標籤
    if (selectedType === 'income') {
      updateTypeLabels('income', 'expense');
      if (selectedLabel == 'chicken') {
          toggleItemVisibility('.chicken_income_item', true);
          toggleItemRequired('.chicken_income_item', true);
      }
      toggleItemVisibility('.expense_item', false);
      toggleItemRequired('.expense_item', false);
    } else if (selectedType === 'expense') {
      updateTypeLabels('expense', 'income');
      toggleItemVisibility('.chicken_income_item', false);
      toggleItemRequired('.chicken_income_item', false);
      toggleItemVisibility('.expense_item', true);
      toggleItemRequired('.expense_item', true);
    }
  });

  // 切換馥香雞/日料/家庭類別
  $('#tracking_management').on('click', 'input[name="item_name"]', function (e) {
    let selectedType = $(this).val();

    updateCategoryLabels(selectedType);
    switchExpenseOptionsFromCategory(selectedType);
  });

  // 切换表單類型
  $('#system_management').on('click', 'input[name="type"]', function (e) {
    let selectedType = $(this).val();
    const typeLabels = {
      'chicken': '馥香雞',
      'hotpot': '日料',
      'home': '家庭',
    };

    // 更新標籤內容及顯示選中狀態
    for (const type in typeLabels) {
      const label = $(`label[for="type_${type}"]`);
      if (type === selectedType) {
        label.html(`<i class='fa-solid fa-check'></i>${typeLabels[type]}`);
      } else {
        label.html(typeLabels[type]);
      }
    }
  });

  // 送出按鈕點擊事件處理函數
  function handleSubmitButtonClick(e) {
    e.preventDefault();
    const next = $(this).hasClass('continue_btn') ? 'reload' : 'home';

    // 表單驗證
    const form = $(this).closest('form');
    const isFormValid = checkRequired(form);

    if (!isFormValid) {
      openMsgWindow('remind', '資料不完整', '要填寫完整才能送出唷!', function (e) {});
      return;
    }

    // 提交表單
    const url = form.attr('action');
    const data = form.serialize();

    postAjax(url, data, function (response) {
      if (next === 'reload') {
        window.location.reload();
      } else {
        const cancelBtn = $('.cancel_btn');
        if (cancelBtn.length > 0 && cancelBtn.attr('href')) {
          const backUrl = cancelBtn.attr('href');
          let newUrl = backUrl.split('?')[0] + "?cat=" + response.type;
          window.location.href = newUrl;
        } else {
          const backUrl = cancelBtn.data('url');
          window.location.href = backUrl;
        }
      }
    });
  }

  // 送出表單
  $('#tracking_management, #chicken_management, #hotpot_management, #expense_management, #system_management').on('click', '.submit_btn, .continue_btn', handleSubmitButtonClick);

  // 記帳頁面enter送出表單
  $('#tracking_management').on('keypress', 'form', function(e) {
    if (e.keyCode === 13) {
        e.preventDefault();
    }
  });

  // 刪除按鈕點擊事件處理函數
  function handleDeleteButtonClick(e, confirmMessage, successCallback) {
    let form = $(e.target).closest('form');
    let url = form.attr('action');
    let data = form.serialize();

    openMsgWindow('confirm', '確定要刪除資料嗎?', confirmMessage, function () {
      postAjax(url, data, function (rep) {
        window.location.reload();
        if (typeof successCallback === 'function') {
          successCallback();
        }
      });
    });
  }

  // 刪除單筆資料-報表
  $('#report_management').on('click', '.delete_btn', function (e) {
    handleDeleteButtonClick(e, '刪除後資料將不會保留唷!', null);
  });

  // 刪除單筆資料-設定
  $('#system_management').on('click', '.delete_btn', function (e) {
    handleDeleteButtonClick(e, '確認刪除的話，資料庫中關於這個類別的帳款都會一併刪除唷!', null);
  });

  // 返回
  $('#tracking_management, #chicken_management, #hotpot_management, #expense_management').on('click', '.cancel_btn', function(e) {
    e.preventDefault();
    let url = $(this).data('url');
    window.location.href = url;
  });

  // 切換顏色設定
  $('#system_management').on('click', '.color_btn', function(e) {
    let form = $(this).closest('form');
    let value = $(this).prev().val();
    form.find('input[name="_color"]').val(value);

    let url = form.attr('action');
    let data = form.serialize();
    postAjax(url, data, function(rep) {
      window.location.reload();
    })
  });

  // 登入按鈕點擊事件處理函數
  function handleLoginButtonClick() {
    let form = $(this).closest('form');

    // 表單驗證
    var result_pass = checkRequired(form);
    if (!result_pass) {
      openMsgWindow('remind', '資料不完整', '要填寫完整才能送出唷!', function(e) {});
      return;
    }

    let url = form.attr('action');
    let data = form.serialize();
    postAjax(url, data, function(rep) {
      if (rep.status) {
        window.location.href = rep.next;
      } else {
        handleLoginError(rep.error);
      }
    });
  }

  // 登入錯誤處理函數
  function handleLoginError(errorCode) {
    switch (errorCode) {
      case -1:
        openMsgWindow('remind', '資料不完整', '要填寫完整才能送出唷!', function(e) {});
        break;
      case -2:
        openMsgWindow('remind', '資料不正確', '找不到用戶，請確認一下帳號密碼是否輸入錯誤!', function(e) {});
        break;
    }
  }

  // 登入送出表單
  $('#login_page').on('click', '.btn_ok', handleLoginButtonClick);
  $('#login_page').on('keyup', '.required', function(e) {
    if (e.keyCode === 13) {
      $('#login_page').find('.btn_ok').click();
    }
  });

});