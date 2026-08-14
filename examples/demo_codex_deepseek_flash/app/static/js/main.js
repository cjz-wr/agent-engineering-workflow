// Mini Blog frontend helpers
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    lucide.createIcons();
  }

  initMarkdownEditor();

  // Code block copy buttons
  document.querySelectorAll(".markdown-body pre").forEach((pre) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "copy-code-btn";
    button.textContent = "复制";
    button.addEventListener("click", () => {
      const code = pre.querySelector("code");
      const text = code ? code.innerText : pre.innerText;
      navigator.clipboard.writeText(text).then(() => {
        button.textContent = "已复制";
        setTimeout(() => {
          button.textContent = "复制";
        }, 1500);
      });
    });
    pre.appendChild(button);
  });

  // Reading progress bar (article page)
  const progress = document.getElementById("reading-progress");
  if (progress) {
    const update = () => {
      const doc = document.documentElement;
      const total = doc.scrollHeight - doc.clientHeight;
      const ratio = total > 0 ? doc.scrollTop / total : 0;
      progress.style.width = `${Math.min(100, ratio * 100)}%`;
    };
    window.addEventListener("scroll", update, { passive: true });
    update();
  }

  // Back to top button (article page)
  const topButton = document.getElementById("back-to-top");
  if (topButton) {
    window.addEventListener(
      "scroll",
      () => {
        const visible = window.scrollY >= 300;
        topButton.classList.toggle("hidden", !visible);
        topButton.classList.toggle("flex", visible);
      },
      { passive: true }
    );
    topButton.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
});

/**
 * Markdown editor: toolbar insertion, character/word counts and shortcuts.
 * Works alongside Alpine's x-model by dispatching an input event after edits.
 */
function initMarkdownEditor() {
  const editor = document.querySelector("[data-editor]");
  if (!editor) return;
  const textarea = editor.querySelector("textarea[name='content']");
  if (!textarea) return;

  const charEl = editor.querySelector("[data-char-count]");
  const wordEl = editor.querySelector("[data-word-count]");

  const syncCounts = () => {
    const value = textarea.value || "";
    const cjk = (value.match(/[\u4e00-\u9fff]/g) || []).length;
    const words = (value.replace(/[\u4e00-\u9fff]/g, " ").match(/\S+/g) || []).length;
    if (charEl) charEl.textContent = String(cjk + words);
    if (wordEl) wordEl.textContent = String(words);
  };

  const commit = () => {
    textarea.dispatchEvent(new Event("input", { bubbles: true }));
    textarea.focus();
    syncCounts();
  };

  const wrap = (before, after, sample) => {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selected = textarea.value.slice(start, end) || sample || "";
    textarea.setRangeText(before + selected + after, start, end, "end");
    commit();
  };

  const prefix = (marker) => {
    const start = textarea.selectionStart;
    const lineStart = textarea.value.lastIndexOf("\n", start - 1) + 1;
    textarea.setRangeText(marker, lineStart, lineStart, "start");
    textarea.setSelectionRange(lineStart + marker.length, lineStart + marker.length);
    commit();
  };

  const insert = (text) => {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    textarea.setRangeText(text, start, end, "end");
    commit();
  };

  const link = () => {
    const url = window.prompt("链接地址（URL）");
    if (url == null) return;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const label = textarea.value.slice(start, end) || url;
    textarea.setRangeText(`[${label}](${url})`, start, end, "end");
    commit();
  };

  editor.querySelectorAll("[data-md-wrap]").forEach((button) => {
    button.addEventListener("click", () => wrap(button.dataset.mdWrap, button.dataset.mdWrap, button.dataset.mdSample));
  });
  editor.querySelectorAll("[data-md-before]").forEach((button) => {
    button.addEventListener("click", () => wrap(button.dataset.mdBefore, button.dataset.mdAfter || "", button.dataset.mdSample));
  });
  editor.querySelectorAll("[data-md-prefix]").forEach((button) => {
    button.addEventListener("click", () => prefix(button.dataset.mdPrefix));
  });
  editor.querySelectorAll("[data-md-insert]").forEach((button) => {
    button.addEventListener("click", () => insert(button.dataset.mdInsert));
  });
  editor.querySelectorAll("[data-md-link]").forEach((button) => {
    button.addEventListener("click", link);
  });

  textarea.addEventListener("input", syncCounts);
  textarea.addEventListener("keydown", (event) => {
    if (!(event.ctrlKey || event.metaKey)) return;
    const key = event.key.toLowerCase();
    if (key === "b") {
      event.preventDefault();
      wrap("**", "**", "加粗文字");
    } else if (key === "i") {
      event.preventDefault();
      wrap("*", "*", "斜体文字");
    } else if (key === "k") {
      event.preventDefault();
      link();
    }
  });

  syncCounts();
}
