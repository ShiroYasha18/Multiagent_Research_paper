import requests
import re
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.keras as keras
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module

class DataAnalysisAgent:
    def __init__(self, model):
        self.model = model

    def fetch_paper_results(self, query, max_results=5):
        base_url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }

        response = requests.get(base_url, params=params)
        papers = []

        if response.status_code == 200:
            entries = response.text.split("<entry>")[1:]
            for entry in entries:
                title = entry.split("<title>")[1].split("</title>")[0].strip()
                summary = entry.split("<summary>")[1].split("</summary>")[0].strip()
                link = entry.split("<id>")[1].split("</id>")[0].strip()
                numbers = re.findall(r'\b\d+\.?\d*\b', summary)
                numerical_values = [float(num) for num in numbers]

                if numerical_values:
                    papers.append({"title": title, "values": numerical_values, "link": link})

        return papers

    def compare_findings(self, topic):
        papers = self.fetch_paper_results(topic)
        if len(papers) < 2:
            return "❌ Not enough data for comparison."

        all_values = [num for paper in papers for num in paper["values"]]
        data = pd.DataFrame(all_values, columns=["Numerical Values"])
        mean = np.mean(all_values)
        std_dev = np.std(all_values)
        variance = np.var(all_values)

        result = f"📊 **Research Findings Comparison:**\n"
        for paper in papers:
            result += f"- {paper['title']}: {paper['values']} 🔗 [Source]({paper['link']})\n"

        result += f"\n📈 **Statistical Insights:**\n- Mean Value: {round(mean, 2)}\n- Standard Deviation: {round(std_dev, 2)}\n- Variance: {round(variance, 2)}\n"

        if std_dev > 10:
            result += "\n❗ **Research Gaps Identified:** High variance suggests inconsistencies in experimental methods or data quality."

        # SHAP Explanation
        model = lambda x: np.mean(x, axis=1)
        explainer = shap.Explainer(model, data)
        shap_values = explainer(data)
        shap.summary_plot(shap_values, data, show=False)
        plt.savefig("/Users/ayrafraihan/Desktop/pythonProject11/shap_summary_plot.png")
        plt.close()

        # GradCAM Visualization (Mock example)
        dummy_model = keras.Sequential([keras.layers.InputLayer(input_shape=(32, 32, 3)), keras.layers.Conv2D(32, (3, 3), activation="relu"), keras.layers.GlobalAveragePooling2D(), keras.layers.Dense(1, activation="sigmoid")])
        dummy_image = np.random.random((1, 32, 32, 3)).astype(np.float32)
        self.apply_gradcam(dummy_model, dummy_image, "conv2d")

        result += "\n✅ SHAP and GradCAM explanations generated successfully with visualizations."

        return result

    def apply_gradcam(self, model, image, layer_name):
        grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(layer_name).output, model.output])
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(image)
            loss = predictions[:, 0]

        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
        heatmap = tf.reduce_mean(tf.multiply(pooled_grads, conv_outputs), axis=-1)
        heatmap = np.maximum(heatmap, 0)
        heatmap /= np.max(heatmap)
        plt.matshow(heatmap)
        plt.savefig("/Users/ayrafraihan/Desktop/pythonProject11/gradcam_explanation.png")
        plt.close()

    def summarize_papers(self, topic):
        papers = self.fetch_paper_results(topic)
        if not papers:
            return "No papers found for the given topic."
        
        summary = "📚 **Research Papers Summary**\n\n"
        for i, paper in enumerate(papers, 1):
            summary += f"{i}. **Title:** {paper['title']}\n"
            summary += f"   **Key Numerical Findings:** {', '.join(map(str, paper['values']))}\n"
            summary += f"   **Source:** {paper['link']}\n\n"
        
        # Add statistical overview
        all_values = [num for paper in papers for num in paper['values']]
        if all_values:
            summary += "📊 **Statistical Overview**\n"
            summary += f"- Total Papers: {len(papers)}\n"
            summary += f"- Average Value: {round(np.mean(all_values), 2)}\n"
            summary += f"- Range: {round(min(all_values), 2)} - {round(max(all_values), 2)}\n"
        
        return summary
