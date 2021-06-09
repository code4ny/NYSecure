Vue.component("data-summary", {
  props: {
    floorlist: Object,
    blocklist: Object,
    iss: Object,
    locationsdata: Object,
    updatedtime: String,
  },
  delimiters: ["[[", "]]"],
  template: `
    <div class="content">
         <p style="text-align:left;">
         <span class="tabs" 
                :class="{ activeTab: selectedTab === tab }"
                v-for="(tab, index) in tabs"
                @click="selectedTab = tab"
                :key="tab"
          >[[ tab ]]</span>
          <span style="float:right; padding-bottom: 10px; margin-left:5px">[[ updatedtime ]]</span>
        </p>
        
        <div v-show="selectedTab === 'Table Summary'" class="box">
            <table>
                <tr>
                <th></th>
                <th v-for="floor in Object.values(floorlist)">[[ floor ]]</th>
                <th>Total</th>
                </tr>
                <tr v-for="block in Object.keys(processedblock)">
                <th>[[ blocklist[block] ]]</th>
                <td v-for="floor in Object.keys(processedblock[block])" v-if="processedblock[block][floor] !== null">[[ processedblock[block][floor] ]]</td>
                <td v-else style="background-color:#ebebe4;"></td>
            </table>
        </div>
        

        <div v-show="selectedTab === 'By Blocks'">
            <div v-for="block in Object.keys(processedblock)" class="box">
                <label>[[ blocklist[block] ]]</label>
                <ul>
                    <li v-for="floor in Object.keys(processedblock[block])" v-if="processedblock[block][floor] !== null">
                    <label v-if="floor === 'Total'">Total</label>
                    [[ floorlist[floor] ]]: [[ processedblock[block][floor] ]] people
                    </li>
                </ul>
            </div>
        </div>

        <div v-show="selectedTab === 'By Floor'">
            <div v-for="floor in Object.keys(processedfloor)" class="box">
                <label>[[ floorlist[floor] ]]</label>
                <ul>
                    <li v-for="block in Object.keys(processedfloor[floor])" v-if="processedfloor[floor][block] !== null">
                    <label v-if="block === 'Total'">Total</label>
                    [[ blocklist[block] ]]: [[ processedfloor[floor][block] ]] people
                    </li>
                </ul>
            </div>
        </div>
    
    </div>
    `,
  data() {
    return {
      tabs: ["Table Summary", "By Blocks", "By Floor"],
      selectedTab: "Table Summary",
    };
  },

  computed: {
    processedblock() {
      //Processing input to show data by floors
      if (!this.locationsdata) return {};

      var processedblock = new Object();
      //Creating new objects with appropriate keys to store the data in
      //A dictionary with blocks as keys and dictionary of floors with the no of people as values
      for (let block of Object.keys(this.blocklist)) {
        processedblock[block] = new Object();
        for (let floor of Object.keys(this.floorlist)) {
          processedblock[block][floor] = 0;
        }
        processedblock[block]["Total"] = 0;
      }

      //Processing the given data to return data required
      for (let block of Object.keys(this.locationsdata)) {
        let total = 0;
        for (let floor of Object.keys(this.locationsdata[block])) {
          // console.log(floor)
          processedblock[block][floor] = this.locationsdata[block][floor];
          if (this.locationsdata[block][floor] !== null) {
            total += parseInt(this.locationsdata[block][floor]);
          }
          processedblock[block]["Total"] = total;
        }
      }
      return processedblock;
    },

    processedfloor() {
      //Processing input to show data by floors
      if (!this.locationsdata) return {};

      var processedfloor = new Object();
      //Creating new objects with appropriate keys to store the data in
      //A dictionary with floor levels as keys and dictionary of blocks with the no of people as values
      for (let floor of Object.keys(this.floorlist)) {
        processedfloor[floor] = new Object();
        for (let block of Object.keys(this.blocklist)) {
          processedfloor[floor][block] = 0;
        }
        processedfloor[floor]["Total"] = 0;
      }
      //Processing the given data to return data required
      for (let block of Object.keys(this.locationsdata)) {
        for (let floor of Object.keys(this.locationsdata[block])) {
          if (!(floor === "Total")) {
            if (this.locationsdata[block][floor] !== null) {
              processedfloor[floor]["Total"] += parseInt(
                this.locationsdata[block][floor]
              );
            }
            processedfloor[floor][block] = this.locationsdata[block][floor];
          }
        }
      }
      return processedfloor;
    },
  },
});

var app = new Vue({
  el: "#app",
  delimiters: ["[[", "]]"],
  data: {
    api_URL: "https://nysecure.herokuapp.com/api/v1/locationdata",
    floorlist: {
      1: "Level 1",
      2: "Level 2",
      3: "Level 3",
      4: "Level 4",
      5: "Level 5",
    },
    blocklist: {
      main_block: "Main Building",
      lecture_block: "Lecture Theatres",
      science_block: "Science Labs",
    },
    locationsdata: {},
    updatedtime: "-",
  },
  created() {
    this.getLocations();
    this.update();
    this.timer = setInterval(this.getLocations, 5000);
  },
  methods: {
    async getLocations() {
      console.log("await starting");
      const response = await fetch(this.api_URL);
      const data = await response.json();
      this.update();
      return (this.locationsdata = data);
    },
    cancelAutoUpdate() {
      clearInterval(this.timer);
    },
    update() {
      let months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];
      let days = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
      ];
      let d = new Date();
      let str = "Last updated: ";
      str +=
        days[d.getDay()] +
        ", " +
        months[d.getMonth()] +
        " " +
        d.getDate() +
        " " +
        d.getFullYear() +
        ", ";
      str += d.toLocaleTimeString();
      return (this.updatedtime = str);
    },
  },
  beforeDestroy() {
    this.cancelAutoUpdate();
    // stop the auto-updating
  },
});
