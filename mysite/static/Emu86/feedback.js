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
        var el = form && form.elements ? form.elements[name] : null;
        return el && typeof el.value === 'string' ? el.value : '';
    }

    function openMailto(form) {
        if (!form) return;
        var to = (form.getAttribute('data-to') || '').trim();
        if (!to) {
            alert('Feedback address is not configured.');
            return;
        }

        var subject = encodeURIComponent(getFieldValue(form, 'subject').trim());
        var bodyEnc = encodeURIComponent(
            'From: ' + getFieldValue(form, 'realname') +
            '\nEmail: ' + getFieldValue(form, 'email') +
            '\n\n' + getFieldValue(form, 'body')
        );
        var href = 'mailto:' + to + '?subject=' + subject + '&body=' + bodyEnc;
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

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bindFeedbackForm);
    } else {
        bindFeedbackForm();
    }
})();
