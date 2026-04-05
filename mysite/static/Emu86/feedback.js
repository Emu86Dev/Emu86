(function () {
    function findSubmitButton(node) {
        var cur = node;
        while (cur && cur !== document) {
            var tag = cur.tagName;
            var type = cur.type;
            var isInputSubmit = tag === 'INPUT' && type === 'submit';
            var isButtonSubmit = tag === 'BUTTON' && type === 'submit';
            if (isInputSubmit || isButtonSubmit) {
                return cur;
            }
            cur = cur.parentNode;
        }
        return null;
    }

        function getFieldValue(form, name) {
        if (!form || !form.querySelector) return '';
        var el = form.querySelector('[name="' + name + '"]');
        return el && typeof el.value === 'string' ? el.value : '';
    }

        function openMailto(form) {
        if (!form) return;
        var to = (form.getAttribute('data-to') || '').trim();
        if (!to) {
            alert('Feedback address is not configured.');
            return;
        }

        var fd = new FormData(form);
        var realname = String(fd.get('realname') || '');
        var email = String(fd.get('email') || '');
        var subjectRaw = String(fd.get('subject') || '').trim();
        var message = String(fd.get('body') || '');
        alert("realname: " + realname + " email: " + email + " subject: " + subjectRaw + " message: " + message);
        var bodyRaw =
            'From: ' + realname +
            '\r\nEmail: ' + email +
            '\r\n\r\n' + message;

        var parts = [];
        if (subjectRaw) parts.push('subject=' + encodeURIComponent(subjectRaw));
        if (bodyRaw) parts.push('body=' + encodeURIComponent(bodyRaw));
        var href = 'mailto:' + to + (parts.length ? ('?' + parts.join('&')) : '');
        window.location.href = href;
    }

    function bindFeedbackForm() {
        var form = document.getElementById('feedback-form');
        if (!form) return;

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            openMailto(form);
        });

        document.addEventListener('click', function (e) {
            var t = e ? e.target : null;
            if (!t) return;
            if (t.nodeType === 3) t = t.parentNode; // text node safety
            var btn = findSubmitButton(t);
            if (!btn) return;
            var targetForm = btn.form || document.getElementById('feedback-form');
            if (!targetForm || targetForm.id !== 'feedback-form') return;
            e.preventDefault();
            openMailto(targetForm);
        }, true);
        
    }
        function fieldById(id) {
        var el = document.getElementById(id);
        return el && typeof el.value === 'string' ? el.value : '';
    }

    function openMailto(form) {
        if (!form) return;
        var to = (form.getAttribute('data-to') || '').trim();
        if (!to) {
            alert('Feedback address is not configured.');
            return;
        }

        var fd = new FormData(form);
        var realname = String(fd.get('realname') || fieldById('feedback-realname') || '');
        var email = String(fd.get('email') || fieldById('feedback-email') || '');
        var subjectRaw = String(fd.get('subject') || fieldById('feedback-subject') || '').trim();
        var message = String(fd.get('body') || fieldById('feedback-body') || '');
        var bodyRaw =
            'From: ' + realname +
            '\r\nEmail: ' + email +
            '\r\n\r\n' + message;

        var parts = [];
        if (subjectRaw) parts.push('subject=' + encodeURIComponent(subjectRaw));
        if (bodyRaw) parts.push('body=' + encodeURIComponent(bodyRaw));
        var href = 'mailto:' + to + (parts.length ? ('?' + parts.join('&')) : '');
        window.location.href = href;
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bindFeedbackForm);
    } else {
        bindFeedbackForm();
    }
})();
