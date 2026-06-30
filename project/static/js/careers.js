// Careers: submit a job application (multipart, resume upload) to the API.
(function () {
  "use strict";
  var form = document.getElementById("application-form");
  if (!form) return;
  var alertBox = document.getElementById("apply-alert");
  var btn = document.getElementById("apply-btn");
  var btnText = document.getElementById("apply-text");
  var spinner = document.getElementById("apply-spinner");

  function show(msg, ok) {
    alertBox.className = "mt-3 alert " + (ok ? "alert-success" : "alert-danger");
    alertBox.textContent = msg;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.classList.add("was-validated"); return; }
    var data = new FormData();
    data.append("opening", document.getElementById("opening").value);
    data.append("name", document.getElementById("name").value);
    data.append("email", document.getElementById("email").value);
    data.append("phone", document.getElementById("phone").value);
    data.append("cover_letter", document.getElementById("cover_letter").value);
    var resume = document.getElementById("resume").files[0];
    if (resume) data.append("resume", resume);

    btn.disabled = true; btnText.textContent = "Submitting..."; spinner.classList.remove("d-none");
    try {
      var res = await fetch("/api/v1/applications/", { method: "POST", body: data });
      if (res.status === 201) {
        form.reset(); form.classList.remove("was-validated");
        show("Application submitted. Our HR team will be in touch. Check your email for a confirmation.", true);
      } else if (res.status === 429) {
        show("Too many submissions. Please try again later.", false);
      } else {
        var err = await res.json();
        show(Object.values(err).flat().join(" ") || "Something went wrong.", false);
      }
    } catch (_) {
      show("Network error. Please try again.", false);
    } finally {
      btn.disabled = false; btnText.textContent = "Submit Application"; spinner.classList.add("d-none");
    }
  });
})();
