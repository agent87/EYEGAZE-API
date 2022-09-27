function close_exam() {
    return new Promise((resolve, reject) => {
      $.getJSON({
        url: "http://127:0:0:1:8000",
        success: resolve,
        error: reject,
      });
    });
  }