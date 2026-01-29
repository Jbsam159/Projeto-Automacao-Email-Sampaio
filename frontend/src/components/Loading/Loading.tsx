type LoadingProps = {
  text?: string;
};

export function Loading({ text = "Processando..." }: LoadingProps) {
  return (
    <div className="loading">
      <span className="spinner" />
      <span>{text}</span>
    </div>
  );
}
