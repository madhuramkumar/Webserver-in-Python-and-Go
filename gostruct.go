package main

import (
    "fmt"
    "log"
    "net/http"
    "io/ioutil"
    "encoding/json"
)

type Catalog struct {
  d map[string]int
}

func NewCatalog() Catalog {
  d := make(map[string]int)
  return Catalog{d: d}


func printCatalog(w http.ResponseWriter) {
  fmt.Fprintln(w, "Item ", "Count")
    for key, value := range Catalog {
      fmt.Fprintln(w, key, " ", value)
    }
  }

func readFile() {
  data, _ := ioutil.ReadFile("catalog.txt")
  json.Unmarshal(data, &Catalog)
}

func writeFile() {
  data, _ := json.Marshal(Catalog)
  _ = ioutil.WriteFile("catalog.txt", data, 0644)
}

func handleAdd(w http.ResponseWriter, r *http.Request) {
  //fmt.Fprintln(w, "Adding...")
  item := r.URL.Query().Get("item")
  count := r.URL.Query().Get("count")
  if item != "" && count != "" {
    Catalog[item] = count
    writeFile()
  }

func handleList(w http.ResponseWriter, r *http.Request) {
  printCatalog(w)
}
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
