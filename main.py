from src.graph import build_graph
from datetime import datetime
import os


def save_report(topic, report):
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/{topic.replace(' ','_')}_{timestamp}.md"
    with open(filename,"w",encoding='utf-8') as f:
        f.write(f"# Research Report: {topic}\n\n")
        f.write(report)
    
    return filename

def main():
    graph = build_graph()
    topic = input("Enter research topic: ")
    print("\nResearching... please wait\n")
    result = graph.invoke({"topic": topic})
    report = result['report']
    print("=" * 50)
    print(result["report"])
    print("=" * 50)
    filename = save_report(topic, report)
    print(f"\nReport saved to: {filename}")


if __name__ == "__main__":
    main()