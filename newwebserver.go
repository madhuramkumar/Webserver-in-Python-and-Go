package main

import (
    "fmt"
    "log"
    "net/http"
    "io/ioutil"
    "encoding/json"
)
var myDict = make(map[string]string)

func printCatalog(w http.ResponseWriter) {
  fmt.Fprintln(w, "Item ", "Count")
    for key, value := range myDict {
      fmt.Fprintln(w, key, " ", value)
  }
}

func readFile() {
  data, _ := ioutil.ReadFile("catalog.txt")
  json.Unmarshal(data, &myDict)
}

func writeFile() {
  data, _ := json.Marshal(myDict)
  _ = ioutil.WriteFile("catalog.txt", data, 0644)
}


func main() {
    readFile()
    http.HandleFunc("/", HelloHandler)
    fmt.Println("Server started at port 8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}

func HelloHandler(w http.ResponseWriter, r *http.Request) {
    //fmt.Fprintln(w, r.URL.Path)
    if r.URL.Path == "/catalog/add" {
      handleAdd(w, r)
    } else if r.URL.Path == "/catalog/list" {
      handleList(w, r)
    }
}

func handleAdd(w http.ResponseWriter, r *http.Request) {
  //fmt.Fprintln(w, "Adding...")
  item := r.URL.Query().Get("item")
  count := r.URL.Query().Get("count")
  if item != "" && count != "" {
    myDict[item] = count
    writeFile()

  }

}

func handleList(w http.ResponseWriter, r *http.Request) {
  //fmt.Fprintln(w, "Listing..")
  printCatalog(w)
}
