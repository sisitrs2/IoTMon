package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/cookiejar"
	"net/url"
	"os"
	"sync"

	"github.com/PuerkitoBio/goquery"
)

type Device struct {
	Name        string `json:"name"`
	Address     string `json:"address"`
	Type        string `json:"type"`
	Version     string `json:"version"`
	Status      string `json:"status"`
	Temperature string `json:"temperature"`
	Voltage     string `json:"voltage"`
	Current     string `json:"current"`
	Alarm       string `json:"alarm"`
	Link        string `json:"link"`
	Username    string `json:"username"`
	Password    string `json:"password"`
	LastScan    string `json:"lastscan"`
}

func Login(device Device, res *http.Response, client *http.Client) *goquery.Document {
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
}

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
	_ = Login(*device, res, client)
	//TODO: Scrape device
	device.LastScan = "01/01/1970 00:00:00"
}

func main() {
	jsonFile, err := os.Open("map.json")
	if err != nil {
		log.Fatal(err)
	}
	defer jsonFile.Close()
	var wg sync.WaitGroup
	byteValue, _ := ioutil.ReadAll(jsonFile)
	var devices []Device
	err = json.Unmarshal(byteValue, &devices)
	if err != nil {
		log.Fatal(err)
	}
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
