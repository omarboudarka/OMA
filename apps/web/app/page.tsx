import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center gap-4 p-8">
      <h1 className="text-2xl font-semibold">OMA</h1>
      <p className="text-muted-foreground">
        AI study assistant. Nothing to see yet.
      </p>
      <Button disabled>Upload a course (soon)</Button>
    </main>
  );
}
