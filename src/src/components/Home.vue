<template>
  <div>
    <el-row class="emotion-editor">
      <el-col :md="{ span: 20, offset: 2 }">
        <quill-editor
          v-model="content"
          ref="myQuillEditor"
          :options="editorOption"
          @change="onEditorChange($event)"
        ></quill-editor>
      </el-col>
    </el-row>

    <el-row class="emotion-submit">
      <el-col style="text-align:center">
        <el-button type="primary" :loading="predicting" @click="submitPrediction">Predict Now</el-button>
        <el-button type="primary" :loading="predicting" @click="demoText">Demo</el-button>
      </el-col>
    </el-row>

    <el-row class="emotion-output">
      <el-col :md="{ span: 18, offset: 4 }">
        <el-row>
          <p class="emotion-title"></p>
        </el-row>
        <el-row>
          <el-col :span="8" class="box-card">
            <el-card>
              <div slot="header" class="clearfix">
                <span>Valence</span>
              </div>
              <div>
                <el-progress
                  type="circle"
                  :percentage="Math.round(emotionOutput.valence/emotionOutput.aTotal * 100) || 50"
                ></el-progress>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8" class="box-card">
            <el-card>
              <div slot="header" class="clearfix">
                <span>Arousal</span>
              </div>
              <div>
                <el-progress
                  type="circle"
                  :percentage="Math.round(emotionOutput.arousal/emotionOutput.aTotal * 100) || 50"
                  color="#11a683"
                ></el-progress>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8" class="box-card">
            <el-card>
              <div slot="header" class="clearfix">
                <span>Dominance</span>
              </div>
              <div>
                <el-progress
                  type="circle"
                  :percentage="Math.round(emotionOutput.dominance/emotionOutput.dTotal * 100) || 50"
                  color="#ec2c4d"
                ></el-progress>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-col :span="6" class="emotion-category">
          <span>Affection</span>
          <el-progress
            :percentage="calculatePercentage(emotionOutput.affection, emotionOutput.categoryTotal)"
            color="#e381e0"
          ></el-progress>
        </el-col>
        <el-col :span="6" class="emotion-category">
          <span>Anger</span>
          <el-progress
            :percentage="calculatePercentage(emotionOutput.anger, emotionOutput.categoryTotal)"
            color="#34acba"
          ></el-progress>
        </el-col>
        <el-col :span="6" class="emotion-category">
          <span>Bravery</span>
          <el-progress
            :percentage="calculatePercentage(emotionOutput.bravery, emotionOutput.categoryTotal)"
            color="#ee6a7c"
          ></el-progress>
        </el-col>
        <el-col :span="6" class="emotion-category">
          <span>Fear</span>
          <el-progress
            :percentage="calculatePercentage(emotionOutput.fear, emotionOutput.categoryTotal)"
            color="#ffa7a5"
          ></el-progress>
        </el-col>
        <el-col :span="6" class="emotion-category">
          <span>Happiness</span>
          <el-progress
            :percentage="calculatePercentage(emotionOutput.happiness, emotionOutput.categoryTotal)"
            color="#ffe07e"
          ></el-progress>
        </el-col>
        <el-col :span="6" class="emotion-category">
          <span>Neutral</span>
          <el-progress
            :percentage="calculatePercentage(emotionOutput.neutral, emotionOutput.categoryTotal)"
            color="#ffe7d6"
          ></el-progress>
        </el-col>
        <el-col :span="6" class="emotion-category">
          <span>Sadness</span>
          <el-progress
            :percentage="calculatePercentage(emotionOutput.sadness, emotionOutput.categoryTotal)"
            color="#72dcbb"
          ></el-progress>
        </el-col>
        <el-col :span="6" class="emotion-category">
          <span>Surprise</span>
          <el-progress
            :percentage="calculatePercentage(emotionOutput.surprise, emotionOutput.categoryTotal)"
            color="#1fd158"
          ></el-progress>
        </el-col>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";
import "quill/dist/quill.bubble.css";
import { quillEditor } from "vue-quill-editor";
// import Quill from "quill";

export default {
  components: {
    quillEditor
  },
  data() {
    return {
      content: "",
      editorOption: {
        theme: "bubble",
        placeholder: "Tell me about your story..."
      },
      formStory: {
        story: ""
      },
      sentences: [],
      colorizedSentences: [],
      emotionOutput: {
        valence: 0,
        arousal: 0,
        dominance: 0,
        affection: 0,
        anger: 0,
        bravery: 0,
        fear: 0,
        happiness: 0,
        neutral: 0,
        sadness: 0,
        surprise: 0,
        vTotal: 0,
        aTotal: 0,
        dTotal: 0,
        categoryTotal: 0
      },
      predicting: false,
      predicted: [],
      customStyle: "",
      styleDom: "",
      sentenceEmotion: []
    };
  },
  methods: {
    // onEditorBlur(quill) {
    //   console.log("editor blur!", quill);
    // },
    // onEditorFocus(quill) {
    //   console.log("editor focus!", quill);
    // },
    // onEditorReady(quill) {
    //   console.log("editor ready!", quill);
    // },
    resetOutput() {
      // Split this out
      this.emotionOutput.valence = 0;
      this.emotionOutput.arousal = 0;
      this.emotionOutput.dominance = 0;
      this.emotionOutput.vTotal = 0;
      this.emotionOutput.aTotal = 0;
      this.emotionOutput.dTotal = 0;

      this.emotionOutput.affection = 0;
      this.emotionOutput.anger = 0;
      this.emotionOutput.bravery = 0;
      this.emotionOutput.fear = 0;
      this.emotionOutput.happiness = 0;
      this.emotionOutput.neutral = 0;
      this.emotionOutput.sadness = 0;
      this.emotionOutput.surprise = 0;
      this.emotionOutput.categoryTotal = 0;
    },
    updateOutput(emotions) {
      this.resetOutput();
      emotions.forEach(emotion => {
        // Split this out
        this.emotionOutput.valence += parseFloat(emotion.valence);
        this.emotionOutput.arousal += parseFloat(emotion.arousal);
        this.emotionOutput.dominance += parseFloat(emotion.dominance);
        this.emotionOutput.vTotal += 1;
        this.emotionOutput.aTotal += 1;
        this.emotionOutput.dTotal += 1;

        this.emotionOutput[emotion.category_1] += 0.66;
        this.emotionOutput[emotion.category_2] += 0.33;
        // this.emotionOutput[emotion.category_3] += 1;
        this.emotionOutput.categoryTotal += 0.99;
      });
    },
    async submitPrediction() {
      this.predicting = true;
      this.predicted = [];
      this.sentenceEmotion = [];
      this.updateEditor();

      for (const sentence of this.sentences) {
        // this actually no need await, but to make it a bit delay among sentence, showed the aniamtion, so i await here
        await this.predict(sentence);
      }

      this.predicting = false;
    },
    updateEditor() {
      // Clear html and get pure sentence
      let text = this.content.replace(/<\/?[^>]+(>|$)/g, "");
      this.sentences = text.replace(/([.?!])\s*(?=[A-Z])/g, "$1|").split("|");

      // get normal splited by clearning extra sentence
      let counter = 0;
      this.sentences = this.sentences.map(sentence => {
        counter += 1;
        if (counter >= 6) {
          return "";
          // show warming about 5 sentence
        }
        return sentence;
      });

      // Get Colorized
      counter = 0;
      this.colorizedSentences = this.sentences.map(sentence => {
        counter += 1;
        if (counter >= 6) {
          return "";
          // show warming about 5 sentence
        }
        return "<h" + counter + ">" + sentence + "</h" + counter + ">";
      });
    },
    async colorized(index, emotion) {
      // show color
      this.sentences[index] = this.colorizedSentences[index];
      this.content = this.sentences.join(" ");
      // change the label color
      await new Promise(r => setTimeout(r, 10));
      this.sentenceEmotion.push(emotion);

      // TODO: this part damn unoptimized, optimized it
      for (let i = 0; i < this.sentenceEmotion.length; i++) {
        document.getElementsByClassName("ql-editor")[0].childNodes[
          i
        ].style.backgroundColor = this.getColorByEmotion(
          this.sentenceEmotion[i]
        );
      }
    },
    getColorByEmotion(emotion) {
      switch (emotion) {
        case "affection":
          return "#e381e0";
        case "anger":
          return "#34acba";
        case "bravery":
          return "#ee6a7c";
        case "fear":
          return "#ffa7a5";
        case "happiness":
          return "#ffe07e";
        case "neutral":
          return "#ffe7d6";
        case "sadness":
          return "#72dcbb";
        case "surprise":
          return "#1fd158";
      }
    },
    calculatePercentage(emotionValue, totalValue) {
      let val = ((emotionValue / totalValue) * 100).toFixed(0);
      if (isNaN(val)) {
        return 0;
      } else {
        return parseInt(val);
      }
    },
    onEditorChange({ quill, html, text }) {
      this.content = html;
    },
    async predict(sentence) {
      return axios({
        method: "post",
        url: "http://localhost:5000/api/predict",
        data: {
          sentence: sentence
        }
      }).then(res => {
        this.predicted.push(res.data);
        this.colorized(this.predicted.length - 1, res.data.category_1);
        this.updateOutput(this.predicted);
        document.getElementsByClassName("emotion-title")[0].innerHTML = "";
        return res.data;
      });
    },
    changeEmotionOutput(index) {
      // show by index
      this.updateOutput([this.predicted[index]]);
      document.getElementsByClassName("emotion-title")[0].innerHTML = "Sentence " + (index + 1);
      this.$notify({
        // title: 'Sentence ' + (index + 1),
        duration: 2000,
        message: 'Display sentence ' + (index + 1) + " emotion",
        // type: 'success'
      });
    },
    initSentenceClick() {
      document.body.addEventListener("click", element => {
        if (element.target.classList.contains("quill-editor")) {
          this.updateOutput(this.predicted);
          document.getElementsByClassName("emotion-title")[0].innerHTML = "";
          this.$notify({
            // title: 'Sentence ' + (index + 1),
            duration: 2000,
            message: "Display overall emotion",
            // type: 'success'
          });
        } else if (element.target.nodeName === "H1") {
          this.changeEmotionOutput(0);
        } else if (element.target.nodeName === "H2") {
          this.changeEmotionOutput(1);
        } else if (element.target.nodeName === "H3") {
          this.changeEmotionOutput(2);
        } else if (element.target.nodeName === "H4") {
          this.changeEmotionOutput(3);
        } else if (element.target.nodeName === "H5") {
          this.changeEmotionOutput(4);
        }
      });
    },
    demoText() {
      this.content =
        "She gave him the mirror in his hand, and he saw there in the likeness of the most beautiful maiden on earth.If that is the ladder by which one mounts, i too will try my fortune.Suddenly something amazing happened.We dare not obey your orders.The place burnt like fire, and the poison entered into his blood fear";
      this.submitPrediction();
    }
  },
  computed: {
    editor() {
      return this.$refs.myQuillEditor.quill;
    }
  },
  mounted() {
    this.resetOutput();
    this.initSentenceClick();
    this.styleDom = document.createElement("style");
  }
};
</script>

<style>
.emotion-editor {
  min-height: 400px;
}

.emotion-submit {
  margin: 20px;
}

.emotion-category {
  padding: 20px;
}

.emotion-output {
  background: #f0f2fc;
  padding: 5px 40px;
  text-align: center;
}

.emotion-title {
  padding: 10px 0 0 0;
}

.quill-editor {
  padding: 100px;
  font-size: 20px;
  color: #444444;
  line-height: 1.7;
}

.box-card {
  padding: 5px;
}

.ql-tooltip {
  display: none;
}

.ql-editor p,
.ql-editor h1,
.ql-editor h2,
.ql-editor h3,
.ql-editor h4,
.ql-editor h5 {
  font-size: 20px !important;
  font-weight: normal;
  color: #444444;
  line-height: 1.7;
  padding: 4px;
  display: inline;
}

/* .ql-editor h1 {
  background: #ee6a7c66;
}

.ql-editor h2 {
  background: #29a0ff66;
}

.ql-editor h3 {
  background: #34acba88;
}

.ql-editor h4 {
  background: #ffe07e66;
}

.ql-editor h5 {
  background: #6b307466;
} */
</style>