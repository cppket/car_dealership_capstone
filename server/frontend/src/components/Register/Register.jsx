import React, { useState } from "react";

export default function Register() {
  const [form, setForm] = useState({
    username: "", first_name: "", last_name: "", email: "", password: ""
  });
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  function update(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setMessage("");
    try {
      // Obtain a CSRF cookie before sending a session-protected POST.
      await fetch("/api/csrf/", { credentials: "same-origin" });
      const csrf = document.cookie.split("; ").find((item) => item.startsWith("csrftoken="))?.split("=")[1];
      const response = await fetch("/api/register/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          ...(csrf ? { "X-CSRFToken": decodeURIComponent(csrf) } : {})
        },
        body: JSON.stringify(form)
      });
      const data = await response.json();
      setMessage(response.ok ? "Registration successful. You can now log in." : (data.error || "Registration failed."));
      if (response.ok) setForm({ username: "", first_name: "", last_name: "", email: "", password: "" });
    } catch {
      setMessage("Could not connect to the server. Please try again.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="register-form">
      <h2>Sign up</h2>
      <label>Username<input name="username" value={form.username} onChange={update} autoComplete="username" required /></label>
      <label>First Name<input name="first_name" value={form.first_name} onChange={update} autoComplete="given-name" required /></label>
      <label>Last Name<input name="last_name" value={form.last_name} onChange={update} autoComplete="family-name" required /></label>
      <label>Email<input name="email" type="email" value={form.email} onChange={update} autoComplete="email" required /></label>
      <label>Password<input name="password" type="password" value={form.password} onChange={update} autoComplete="new-password" required minLength={8} /></label>
      <button type="submit" disabled={busy}>{busy ? "Registering..." : "Register"}</button>
      {message && <p role="status">{message}</p>}
    </form>
  );
}
