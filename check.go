package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/cookiejar"
	"sync"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type Device struct {
	Name        string
	Address     string
	Type        string
	Version     string
	Status      string
	Temperature string
	Voltage     string
	Current     string
	Alarm       string
	Link        string
	LastScan    string
}

type DeviceUser struct {
	Username string
	Password string
}

/*func Login(device Device, res *http.Response, client *http.Client) *goquery.Document {
	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		log.Fatal(err)
	}

	loginURL := device.Link + doc.Find("Form").AttrOr("action", "")
	data := url.Values{
		"username": {device.Username},
		"password": {device.Password},
	}
	response, err := client.PostForm(loginURL, data)

	if err != nil {
		log.Fatalln(err)
	}

	defer response.Body.Close()
	doc, err = goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		log.Fatal(err)
	}
	return doc
}*/

func ScrapeDevice(device *Device) {
	// Create HTTP Client with Cookie Jar (for login)
	jar, _ := cookiejar.New(nil)
	client := &http.Client{
		Jar: jar,
	}
	// Request the Device HTML Page.
	res, err := client.Get(device.Link)
	if err != nil {
		device.Status = "Inactive"
		device.Temperature = "Unknown"
		device.Voltage = "Unknown"
		device.Current = "Unknown"
		device.LastScan = "Unknown"
		return
	}
	defer res.Body.Close()

	// Login and Load the Device HTML document
	//_ = Login(*device, res, client)
	//TODO: Scrape device
	device.LastScan = "01/01/1970 00:00:00"
}

func main() {
	db, err := gorm.Open(sqlite.Open(`DB\iotmon.db`), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}
	db.AutoMigrate(&Device{})

	var wg sync.WaitGroup
	var devices []Device
	res := db.Find(&devices)
	fmt.Println(res.)

	for i := 0; i < len(devices); i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			ScrapeDevice(&devices[i])
		}(i)
	}
	wg.Wait()
	newjson, _ := json.MarshalIndent(devices, "", "   ")
	_ = ioutil.WriteFile("map.json", newjson, 0644)
}
