

## Field Definitions

<dl>
    <dt>accuracy_assessment_uri</dt>
    <dd>
        <ul>
            <li>A Uniform Resource Identifier for an HTML document that describes the source, precision, and accuracy of the coordinates provided for a particular location.</li>
            <li>Applies to: locations.csv</li>
        </ul>
    </dd>
    <dt>accuracy_radius</dt>
    <dd>
        <ul>
            <li>Distance in meters indicating the presumed horizontal accuracy of the coordinates provided for a particular location.</li>
            <li>Applies to: locations.csv</li>
        </ul>
    </dd>
    <dt>archaeological_remains</dt>
    <dd>
        <ul>
            <li>Term indicating whether archaeological remains are known to be visible at a particular location and, if so, how substantive they are.</li>
            <li>Terms and definitions: archaeological_remains.csv</li>
            <li>Applies to: locations.csv</li>
        </ul>
    </dd>
    <dt>association_certainty</dt>
    <dd>
        <ul>
            <li>Term indicating the level of certainty in the association between a place and a name, location, or connection.</li>
            <li>Terms and definitions: association_certainty.csv</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv.</li>
        </ul>
    </dd>
    <dt>attested_form</dt>
        <ul>
            <li>Transcription of the attested form of the name in its original language and script (Unicode characters), if known.</li>
            <li>Applies to: names.csv</li>
        </ul>
    <dd></dd>
    <dt>bounding_box_wkt</dt>
        <ul>
            <li>A bounding box for the geometries of all locations associated with a given place.</li>
            <li>Format: expressed as a Polygon using the <a href="https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry">Well-Known Text (WKT)</a> format.</li>
        </ul>
    <dd></dd>
    <dt>connection_type</dt>
    <dd>
        <ul>
            <li>Term indicating the nature of a connection between two places.</li>
            <li>Terms and definitions: connection_types.csv</li>
            <li>Applies to: connections.csv.</li>
        </ul>
    </dd>
    <dt>connects_to</dt>
    <dd>
        <ul>
            <li>Uniform Resource Identifier of the Pleiades place that is the object of a connection.</li>
            <li>Applies to: connections.csv.</li>
        </ul>    
    </dd>
    <dt>created</dt>
    <dd>
        <ul>
            <li>Date and time the record was created in the Pleiades gazetteer.</li>
            <li>Format: A date-time string conforming to the <a href="https://en.wikipedia.org/wiki/ISO_8601">ISO 8601 Date and Time Format</a>, e.g. "2016-07-13T13:31:46Z". All date-times are calculated to the second in <a href="https://en.wikipedia.org/wiki/Coordinated_Universal_Time">Coordinated Universal Time (UTC)</a> and the "Z" timezone indicator is appended.</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>
    </dd>
    <dt>description</dt>
    <dd>
        <ul>
            <li>A English-language description of a particular connection, location, name, or place.</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>
    </dd>
    <dt>details</dt>
    <dd>
        <ul>
            <li>English-language text providing discussion of a particular connection, location, name, or place above and beyond that included in the "description".</li>
            <li>Format: This field may include HTML tags.</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>
    </dd>
    <dt>geometry_wkt</dt>
    <dd>
        <ul>
            <li>Spatial geometry of a particular location.</li>
            <li>Applies to: locations_*.csv.</li>
        </ul>
    </dd>
    <dt>id</dt>
    <dd>
        <ul>
            <li>Alphanumeric identifier for a particular connection, name, location, or place. Can be used together with "place_id" to join connections, names, and locations with the corresponding place data.</li>
            <li>Note: A given "id" value is unique within the CSV file in which is appears; however, "id" uniqueness in the Pleiades webapp is contextual. Therefore, to obtain a completely unique identifier for any item in the Pleiades dataset, use its "uri" value rather than its "id" value.
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>
    </dd>
    <dt>language_tag</dt>
    <dd>
        <ul>
            <li>An alphabetic string indicating the language and writing system of the name contained in the "attested_form" field.</li>
            <li>Format: A string conforming to <a href="https://tools.ietf.org/rfc/bcp/bcp47.txt">IETF BCP 47 Language Tags</a> whose subtags are registered in the <a href="https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry">IANA Language Subtag Registry</a>.</li>
            <li>Terms and definitions: all language tags appearing in Pleiades data are defined in languages_and_scripts.csv.</li>
            <li>Applies to: names.csv.</li>
        </ul>
    </dd>
    <dt>name_type</dt>
    <dd>
        <ul>
            <li>Term indicating the type or function of a name string as recorded in Pleiades.</li>
            <li>Terms and definitions: name_types.csv.</li>
            <li>Applies to: names.csv.</li>
        </ul>
    </dd>
    <dt>place_id</dt>
    <dd>
        <ul>
            <li>An alphabetic string providing the "id" value for the place with which a particular connection, location, or name is associated. In the case of a connection, this is the place **from which** the connection originates. This field can be used to join data about related connections, names, locations, and places.</li>
            <li>Applies to: connections.csv, locations_*.csv, and names.csv.</li>
        </ul>
    </dd>
    <dt>provenance</dt>
    <dd>
        <ul>
            <li>A short textual statement indicating the origin of the data represented in the record.</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>
    </dd>
    <dt>representative_latitude</dt>
    <dd>
        <ul>
            <li>A latitude coordinate, for <a href="https://pleiades.stoa.org/help/representative-points">a Pleiades "representative point"</a> for a place.</li>
            <li>Format: this coordinate is expressed in signed digital degrees and measured according to the <a href="https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84">World Geodetic System, 1984 version (WGS84)</a>.</li>
            <li>Applies to: places.csv.</li>
        </ul>
    </dd>
    <dt>representative_longitude</dt>
    <dd>
        <ul>
            <li>A latitude coordinate, for <a href="https://pleiades.stoa.org/help/representative-points">a Pleiades "representative point"</a> for a place.</li>
            <li>Format: this coordinate is expressed in signed digital degrees and measured according to the <a href="https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84">World Geodetic System, 1984 version (WGS84)</a>.</li>
            <li>Applies to: places.csv.</li>
        </ul>
    </dd>
    <dt>romanized_form_1</dt>
    <dd>
        <ul>
            <li>A romanized form of a name for a Pleiades place.</li>
            <li>Note: this field may have a value even if the "attested_form" for a name is blank. When a value is provided in "attested_form", this value is a romanization of that form. Otherwise, this form has been recorded from a secondary source in which the original language and script are not provided (or if the script used originally was not yet supported by the Unicode standard at the time the record was created.)
            <li>Applies to: names.csv.</li>
        </ul>
    </dd>
    <dt>romanized_form_2</dt>
    <dd>
        <ul>
            <li>An alternate romanized form for a name. See "romanized_form_1".</li>
            <li>Applies to: names.csv.</li>
        </ul>
    </dd>
    <dt>romanized_form_3</dt>
    <dd>
        <ul>
            <li>An alternate romanized form for a name. See "romanized_form_1".</li>
            <li>Applies to: names.csv.</li>
        </ul>
    </dd>
    <dt>title</dt>
    <dd>
        <ul>
            <li>An alphanumeric string providing a title for a particular connection, location, name, or place. For more information about naming conventions in Pleiades, see "<a href="https://pleiades.stoa.org/help/editorial-guidelines#section-2">About Titles</a>" in the *Pleiades Editorial Guidelines.*</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>
    </dd>
    <dt>transcription_accuracy</dt>
    <dd>
        <ul>
            <li>A term indicating the level of accuracy thought to obtain with respect to the witness tradition of a particular name variant (i.e., whether or not it has been transmitted to us correctly).</li>
            <li>Terms and definitions: transcription_accuracy.csv.</li>
            <li>Applies to: names.csv.</li>
        </ul>
    </dd>
    <dt>transcription_completeness</dt>
    <dd>
        <ul>
            <li>Term indicating whether the witness tradition of a particular name variant has brought us the name in complete form, or if it is fragmentary.</li>
            <li>Terms and definitions: transcription_completeness.csv.</li>
            <li>Applies to: names.csv.</li>
        </ul>
    </dd>
    <dt>uri</dt>
    <dd>
        <ul>
            <li>A Uniform Resource Identifier uniquely identifying a particular connection, location, name, or place.</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>        
    </dd>
    <dt>year_after_which</dt>
    <dd>
        <ul>
            <li>The year after which a particular connection, location, name, or place flourished, was in use, or otherwise obtained, i.e., <i><a href="https://en.wikipedia.org/wiki/Terminus_post_quem">terminus post quem</a></i>.</li>
            <li>Format: a signed integer indicating a year in the <a href="https://en.wikipedia.org/wiki/Proleptic_Julian_calendar">proleptic Julian calendar</a>. There is no <a href="https://en.wikipedia.org/wiki/Year_zero">year zero</a>.</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>
    </dd>
    <dt>year_before_which</dt>
    <dd>
        <ul>
            <li>The year before which a particular connection, location, name, or place flourished, was in use, or otherwise obtained, i.e., <i>terminus ante quem</i>.</li>
            <li>Format: a signed integer indicating a year in the <a href="https://en.wikipedia.org/wiki/Proleptic_Julian_calendar">proleptic Julian calendar</a>. There is no <a href="https://en.wikipedia.org/wiki/Year_zero">year zero</a>.</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
    </dd>
</dl>