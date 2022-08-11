package main

import (
	"fmt"
	"log"
	"net/http"
	"net/http/cookiejar"
	"net/url"
	"sync"
	"time"

	"github.com/PuerkitoBio/goquery"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type Device struct {
	ID           uint
	Name         string
	Address      string
	TypeId       uint
	Version      string
	Temperature  string
	Voltage      string
	Current      string
	Status       string
	Data         string
	Lastscan     string
	Link         string
	DeviceUserId uint
	AreaId       uint
}

type DeviceUser struct {
	Username    string
	Password    string
	TypeId      string
	Permissions string
}

func Login(device Device, res *http.Response, client *http.Client) *goquery.Document {
	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		log.Fatal(err)
	}

	loginURL := device.Link + doc.Find("Form").T

	data := url.Values{}
	data.Add("Username", "name")
	data.Add("Password", "pass")

	response, err := client.PostForm(loginURL, data)

	if err != nil {
		log.Fatalln(err)
	}

	defer response.Body.Close()
	doc, err = goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		log.Fatal(err)
	}
	doc.Find("AA")
	return doc
}

func ScrapeDevice(device *Device) {
	// Create HTTP Client with Cookie Jar (for login)

	jar, _ := cookiejar.New(nil)
	client := &http.Client{
		Jar: jar, Timeout: 2 * time.Second,
	}
	// Request the Device HTML Page.
	res, err := client.Get(device.Link)
	if err != nil {
		device.Status = "Unaccessable"
		device.Temperature = ""
		device.Voltage = ""
		device.Current = ""
		device.Lastscan = (time.Now()).Format("2006/01/02 15:04:05")
		return
	}
	defer res.Body.Close()
	if device.TypeId == 1 {
		//doc := Login(*device, res, client)
		//doc = doc
	}
	if device.TypeId == 2 {
	}

	device.Lastscan = (time.Now()).Format("2006/01/02 15:04:05")
	device.Name = "Ilay"
}

func main() {
	db, err := gorm.Open(sqlite.Open(`DB\iotmon.db`), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}
	//var wg sync.WaitGroup
	var devices []Device
	_ = db.Find(&devices)
	var wg sync.WaitGroup

	for i := 0; i < len(devices); i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			ScrapeDevice(&devices[i])
			fmt.Println(i)
		}(i)
	}
	wg.Wait()
	for _, device := range devices {
		db.Save(&device)
	}
}
