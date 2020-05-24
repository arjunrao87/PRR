<template>
  <div class="container">
    <h3>HARO (Help A Reporter Out)</h3>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Category</th>
          <th scope="col">Summary</th>
          <th scope="col">Name</th>
          <th scope="col">Media outlet</th>
          <th scope="col">Email</th>
          <th scope="col">Deadline date</th>
          <th scope="col">Deadline time</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="story in stories" v-bind:key="story.id"> 
          <td>{{story.get('category')}}</td>
          <td>{{story.get('summary')}}</td>
          <td>{{story.get('name')}}</td>
          <td>{{story.get('media_outlet')}}</td>
          <td>{{story.get('email')}}</td>
          <td>{{story.get('deadline_date')}}</td>
          <td>{{story.get('deadline_time')}}</td>
        </tr>
      </tbody>
    </table> 
  </div> 
</template>

<script>
var Airtable = require('airtable');
var base = new Airtable({apiKey: process.env.VUE_APP_AIRTABLE_API_KEY}).base(process.env.VUE_APP_AIRTABLE_PRR_BASE);
export default {
    name: "Haro",
    data() {
      return {
        stories: null
      };
    },
    created: function(){
      var vm = this;
      let allStories=[]
      base(process.env.VUE_APP_AIRTABLE_HARO).select({
          maxRecords: 1000,
          view: "Grid view"
      }).eachPage(function page(records, fetchNextPage) {
          console.log("In the page")
          records.forEach(function(record) {
          console.log("In the recordpush")
            allStories.push(record);
          });
          fetchNextPage();
        }, function done(err) {
            if (err) { console.error(err); return; }
          console.log("In the done")
            vm.stories=allStories;
            return allStories;
        });
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
