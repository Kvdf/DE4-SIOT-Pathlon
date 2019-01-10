function myFunction() {
  //var ss = SpreadsheetApp.getActiveSpreadsheet(); //get active spreadsheet
  var ss = SpreadsheetApp.openByUrl("https://docs.google.com/spreadsheets/d/1yR0BO22F9F7Ek9lWg656l1smV_s5JyKbX7Fyv8pGQ6A/edit#gid=0");
  var sheet = ss.getSheetByName('data'); //get sheet by name from active spreadsheet
  
  
  var apiKey = 'b7182748bf'; //apiKey for weerlive weather api  
  var url = 'http://weerlive.nl/api/json-data-10min.php?key=b7182748bf&locatie=Alkmaar';  //api endpoint as a string 
  
  var response = UrlFetchApp.fetch(url); // get api endpoint
  var json = response.getContentText(); // get the response content as text
  var data = JSON.parse(json); //parse text into json
  
  Logger.log(data); //log data to logger to check
  
  var stats=[]; //create empty array to hold data points
  var date = new Date(); //create new date for timestamp
  
  
  
  
  //The following lines push the parsed json into empty stats array
    stats.push(date);//timestamp 
    stats.push(data.liveweer[0].temp); //temp
    stats.push(data.liveweer[0].lv); //relative humidity
    stats.push(data.liveweer[0].winds); //wind speed (Beaufort) 
    stats.push(data.liveweer[0].d0zon); //chance of sun today(%) 
     
  //append the stats array to the active sheet 
  
  sheet.appendRow(stats);
  // Note in Edit --> Current Project's Timers, I have set a 30 min trigger.
}
