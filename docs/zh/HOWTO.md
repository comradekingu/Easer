指南
======

本指南將描述如何爲Easer添加新功能，如增加新的Event、Condition或Operation，同時也會簡單涉及Easer的設計結構。  
（注意：Profile是一組Operation的集合，所以要擴展Profile只要創建相應的新Operation即可。）

另，v0.7.7新加入`USource`，以便統一Event和Condition的編寫。該機制仍處於早期試驗，故而本文不對其進行描述（但其與之前類似）。

增加Event/Operation
------

在Easer中，所有的Event和Operation都被稱爲*技能*(skill)，均放置於`skills`包下——更具體地，Event在`skills.event`包下，Operation在`skills.operation`包下。

要新建Event或Operation，可以使用提供的腳本，之後自行填充；也可以純手動。

### 使用腳本自動生成模板

在utils目錄下有兩個腳本（`new_event.py`和`new_operation.py`），用於創建相應技能的“模板”——通用部分會被創建，一般而言只需要填充其中TODO部分即可。
做完之後，在`skills.LocalSkillRegistry`中註冊該新技能即完成。

組件的各個部分詳解見下。

### 詳細步驟

要增加新的Event或Operation，本質上來說要做兩件事：

1. 實現新Event或Operation的功能（通過擴展/繼承相應接口，並實現相應內容）
2. 在`skills.LocalSkillRegistry`中註冊該新技能

其中：

* 添加新Event需要繼承`local_skill.eventskill.EventSkill`
* 添加新Operation需要繼承`local_skill.operationskill.OperationSkill`

而在`LocalSkillRegistry`中註冊只需要在其`init()`方法中仿照已有條目，爲新技能寫一行代碼。

強烈建議仿照已有技能的做法，將新的技能放於相應的包/目錄內。

`EventSkill`接口和`OperationSkill`接口均有詳細註釋。

無論是`EventSkill`還是`OperationSkill`均需實現UI部分，均是通過實現一個`skills.SkillViewFragment`的子類來完成。

一些常用的子類已在`skills`或子包中寫好，方便使用。

#### 接口/抽象類作用

`Skill`、`StorageData`爲通用的接口，實際使用中會使用相應的子接口（如`EventSkill`）。每個技能的各個部件均會使用數據，所以其對應數據類（即`StorageData`的子類）需要作爲泛型參數。

* `Skill`/`EventSkill`/`OperationSkill`
	* 技能的入口。所有對技能的使用均始於對入口的函數的調用。
* `StorageData`/`EventData`/`OperationData`
	* 技能的數據。每個實例不會被改變，如要修改則會創建新實例。
	* 一般而言具體的數據（如該類內的域）只會被該技能使用，所以對外界沒有訪問接口。
	* 數據將會被持久化（如保存爲文件），所以定義`serialize()`函數；`parse()`函數見`DataFactory`類。
	* 數據會在Android組件間傳遞，所以實現`Parcelable`接口。
* `DataFactory`/`EventDataFactory`/`OperationDataFactory`
	* 運行時數據由此創建。
	* `parse()`函數用於從之前持久化後的數據中創建相應的`StorageData`對象。
* `SkillViewFragment`
	* 編輯技能的UI，用於和用戶交互。
	* 在“載入”時，如果有初始化數據，則會以該數據爲準而進行UI的初始化。
	* 在“保存”時創建相應`StorageData`，以便後續處理（如持久化）。
* `Slot`/`AbstractSlot`
	* 用於`EventSkill`，負責監聽、通告事件狀態等功能。
	* 一般而言，監聽通過自行設置`BroadcastListener`來完成。
	* 當事件滿足時，調用`changeSatisfiedState()`函數來（向Easer相關組件）通告狀態改變。
	* 當Easer工作時，事件樹上的每個事件均會創建獨立的`Slot`（該行爲有待優化，但目前如此）。
* `OperationLoader`
	* 實施/載入Operation的地方。

