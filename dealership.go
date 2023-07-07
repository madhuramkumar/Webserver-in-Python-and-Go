type autoDealership struct {
  //variable fields defined here
  d map[string]int
}

func newAutoDealership() autoDealership {
  //creating instance of autoDealership class
  d := make(map[string]int)
  return autoDealership{d: d}

func addCar() {
//code to add car
  item := r.URL.Query().Get("car")
  count := r.URL.Query().Get("count")
  if item != "" && count != "" {
    c.d[car] = count

}

func removeCar() {
//code to remove car
  item := r.URL.Query().Get("car")
  count := r.URL.Query().Get("count")
  if item != "" && count != "" {
    del c.d[car]
}

func listCar() {
//code to list car
  fmt.Fprintln(w, "Car", "Count")
    for key, value := c.d {
      fmt.Fprintln(w, key, " ", value)
    }

  }
}
var c autoDealership

func main() {
//call each function here
c = newAutoDealership()
if r.URL.Path == "/catalog/add" {
    addCar(w, r)
} else if r.URL.Path == "/catalog/list" {
    listCar(w, r)
} else if r.URL.Path == "/catalog/remove" {
    removeCar(w, r)
  }
}
