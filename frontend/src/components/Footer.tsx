export function Footer() {
  return (
    <footer className="footer">
      <img
        src="/sampaio_logo.jpg"
        alt="Logo da empresa"
        className="footer-logo"
      />

      <p className="footer-text">
        © {new Date().getFullYear()} Sampaio • Automação de Boletos
      </p>

    </footer>
  );
}
